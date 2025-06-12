from aiohttp import ClientSession, ClientTimeout
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from base58 import b58decode, b58encode
from nacl.signing import SigningKey
from datetime import datetime, timezone
from colorama import *
import asyncio, random, json, os, pytz


init(autoreset=True)
wib = pytz.timezone('Asia/Jakarta')

class BitQuant:
    def __init__(self) -> None:
        self.HEADERS = { "Accept": "*/*", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7", "Origin": "https://www.bitquant.io", "Referer": "https://www.bitquant.io/", "User-Agent": FakeUserAgent().random }
        self.BASE_API = "https://quant-api.opengradient.ai/api"
        self.proxies = []
        self.proxy_index = 0
        self.tokens = {}
        self.id_tokens = {}
        self.initial_questions = ["Hello", "Hi", "What is the price of SOL?", "Tell me about yourself", "What can you do?", "Recommend a token", "How are you?"]

    def log(self, message):
        print(f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now(wib).strftime('%d/%m/%y %H:%M:%S')} ]{Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}", flush=True)

    def welcome(self):
        print(f"""
        {Fore.GREEN + Style.BRIGHT}Auto Multi-Referral BitQuant - BOT
            {Fore.GREEN + Style.BRIGHT}Skrip oleh: {Fore.YELLOW + Style.BRIGHT}scavenger indonesia
            """)

    def generate_solana_wallet(self):
        signing_key = SigningKey.generate()
        full_private_key_bytes = signing_key.encode() + signing_key.verify_key.encode()
        private_key_b58 = b58encode(full_private_key_bytes).decode('utf-8')
        address = b58encode(signing_key.verify_key.encode()).decode('utf-8')
        self.log(f"{Fore.CYAN}Generated New Wallet | Address: {self.mask_account(address)}")
        return private_key_b58, address

    def save_generated_account(self, private_key, address):
        with open('generated_accounts.txt', 'a') as f:
            f.write(f"Address: {address}, PrivateKey: {private_key}\n")
        self.log(f"{Fore.YELLOW}Successfully saved new account to 'generated_accounts.txt'")

    def generate_address(self, account: str):
        try:
            decoded_key = b58decode(account)
            key_bytes = decoded_key[:32] if len(decoded_key) == 64 else decoded_key
            signing_key = SigningKey(key_bytes)
            return b58encode(signing_key.verify_key.encode()).decode()
        except Exception as e:
            self.log(f"{Fore.RED}Error decoding private key: {e}"); return None

    def generate_login_payload(self, account: str, address: str):
        now = datetime.now(timezone.utc)
        nonce = int(now.timestamp() * 1000)
        issued_at = now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        message = f"bitquant.io wants you to sign in with your **blockchain** account:\n{address}\n\nURI: https://bitquant.io\nVersion: 1\nChain ID: solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp\nNonce: {nonce}\nIssued At: {issued_at}"
        decoded_key = b58decode(account)
        key_bytes = decoded_key[:32] if len(decoded_key) == 64 else decoded_key
        signing_key = SigningKey(key_bytes)
        signature = signing_key.sign(message.encode('utf-8'))
        return {"address": address, "message": message, "signature": b58encode(signature.signature).decode()}

    def generate_agent_payload(self, address: str, question: str):
        return {"context": {"conversationHistory": [], "address": address, "poolPositions": [], "availablePools": []}, "message": {"type": "user", "message": question}}
            
    def mask_account(self, account):
        return account[:6] + '*' * (len(account) - 12) + account[-6:] if account else "******"

    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        if use_proxy_choice == 3: return
        try:
            if use_proxy_choice == 1:
                self.log("Downloading free proxies...")
                async with ClientSession(timeout=ClientTimeout(total=30)) as s:
                    async with s.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as r:
                        r.raise_for_status()
                        self.proxies = [line.strip() for line in (await r.text()).splitlines() if line.strip()]
            elif use_proxy_choice == 2:
                if not os.path.exists(filename): self.log(f"{Fore.RED}File {filename} Not Found."); return
                with open(filename, 'r') as f: self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            if self.proxies: self.log(f"{Fore.GREEN}Loaded {len(self.proxies)} proxies.")
        except Exception as e: self.log(f"{Fore.RED}Failed to load proxies: {e}")

    def get_next_proxy_for_account(self):
        if not self.proxies: return None
        proxy = self.proxies[self.proxy_index % len(self.proxies)]
        self.proxy_index += 1
        return f"http://{proxy}" if "://" not in proxy else proxy

    async def _api_call(self, session, method, url, headers, **kwargs):
        try:
            async with session.request(method, url, headers=headers, ssl=False, **kwargs) as response:
                if response.status == 200:
                    try: return await response.json()
                    except: return True 
                self.log(f"{Fore.YELLOW}API call to {url.split('?')[0].split('/')[-1]} failed. Status: {response.status}")
        except Exception as e:
            self.log(f"{Fore.YELLOW}API call failed: {e}")
        return None

    async def process_secure_token(self, account: str, address: str, proxy=None):
        async with ClientSession(connector=ProxyConnector.from_url(proxy) if proxy else None, timeout=ClientTimeout(total=60)) as session:
            login_payload = self.generate_login_payload(account, address)
            login_data = await self._api_call(session, "POST", f"{self.BASE_API}/verify/solana", {**self.HEADERS, "Content-Type": "application/json"}, json=login_payload)
            if login_data and "token" in login_data:
                self.tokens[address] = login_data["token"]
                secure_token_payload = {"token": self.tokens[address], "returnSecureToken": True}
                id_token_data = await self._api_call(session, "POST", f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=AIzaSyBDdwO2O_Ose7LICa-A78qKJUCEE3nAwsM", {**self.HEADERS, "Content-Type": "application/json"}, json=secure_token_payload)
                if id_token_data and "idToken" in id_token_data:
                    self.log(f"{Fore.GREEN}Login Success for {self.mask_account(address)}")
                    return id_token_data["idToken"]
        self.log(f"{Fore.RED}Login process failed for {self.mask_account(address)}"); return None

    async def generate_invite_code(self, id_token: str, address: str, proxy=None):
        headers = {**self.HEADERS, "Authorization": f"Bearer {id_token}"}
        payload = {"address": address}
        async with ClientSession(connector=ProxyConnector.from_url(proxy) if proxy else None) as session:
            return await self._api_call(session, "POST", f"{self.BASE_API}/invite/generate", headers, json=payload)

    async def activate_invite_code(self, main_id_token: str, invite_code: str, referee_address: str, proxy=None):
        self.log(f"Activating invite code for {self.mask_account(referee_address)}...")
        headers = {**self.HEADERS, "Authorization": f"Bearer {main_id_token}"}
        payload = {"code": invite_code, "address": referee_address}
        async with ClientSession(connector=ProxyConnector.from_url(proxy) if proxy else None) as session:
            response = await self._api_call(session, "POST", f"{self.BASE_API}/invite/use", headers, json=payload)
            if response:
                self.log(f"{Fore.GREEN}Invite code successfully activated!")
                return True
            self.log(f"{Fore.RED}Failed to activate invite code.")
            return False

    async def run_first_interaction(self, id_token: str, address: str, proxy=None):
        self.log(f"Performing first interaction for {self.mask_account(address)}...")
        headers = {**self.HEADERS, "Authorization": f"Bearer {id_token}"}
        payload = self.generate_agent_payload(address, random.choice(self.initial_questions))
        async with ClientSession(connector=ProxyConnector.from_url(proxy) if proxy else None) as session:
            response = await self._api_call(session, "POST", f"{self.BASE_API}/agent/run", headers, json=payload)
            if response: self.log(f"{Fore.GREEN}First interaction successful!")
            else: self.log(f"{Fore.RED}First interaction failed.")

    def print_question(self):
        while True:
            try:
                print(f"\n{Fore.WHITE}1. Run With Proxyscrape Free Proxy\n2. Run With Private Proxy (dari proxy.txt)\n3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE+Style.BRIGHT}Pilih Opsi Proxy [1/2/3] -> {Style.RESET_ALL}").strip())
                if choose in [1, 2, 3]: return choose
                self.log(f"{Fore.RED}Pilihan tidak valid.")
            except ValueError: self.log(f"{Fore.RED}Input harus berupa angka.")

    async def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.welcome()
        try:
            main_private_key = input(f"{Fore.YELLOW+Style.BRIGHT}Masukkan Private Key Akun Induk Anda: {Style.RESET_ALL}").strip()
            if not main_private_key: raise ValueError("Private key tidak boleh kosong.")
            num_to_generate = int(input(f"{Fore.YELLOW+Style.BRIGHT}Jumlah akun referral yang ingin dibuat: {Style.RESET_ALL}").strip())
            if num_to_generate <= 0: raise ValueError("Jumlah harus lebih dari 0.")
        except ValueError as e: self.log(f"{Fore.RED}{e}"); return

        use_proxy_choice = self.print_question()
        if use_proxy_choice in [1, 2]: await self.load_proxies(use_proxy_choice)

        self.log(f"{Fore.MAGENTA}{'='*20} MEMPROSES AKUN INDUK {'='*20}{Style.RESET_ALL}")
        main_address = self.generate_address(main_private_key)
        if not main_address: return
        main_id_token = await self.process_secure_token(main_private_key, main_address, self.get_next_proxy_for_account())
        if not main_id_token: return
            
        for i in range(num_to_generate):
            self.log(f"{Fore.MAGENTA}{'='*20} MEMBUAT AKUN REFERRAL #{i+1}/{num_to_generate} {'='*20}{Style.RESET_ALL}")
            self.log("Meminta kode referral baru dari server...")
            proxy_for_invite = self.get_next_proxy_for_account()
            invite_data = await self.generate_invite_code(main_id_token, main_address, proxy_for_invite)
            if not invite_data or "invite_code" not in invite_data:
                self.log(f"{Fore.RED}Gagal mendapatkan kode referral baru. Lanjut ke berikutnya."); continue
            invite_code = invite_data["invite_code"]
            self.log(f"{Fore.GREEN+Style.BRIGHT}Sukses! Menggunakan kode referral baru: {invite_code}")

            referee_pk, referee_address = self.generate_solana_wallet()
            proxy = self.get_next_proxy_for_account()
            is_activated = await self.activate_invite_code(main_id_token, invite_code, referee_address, proxy)
            if not is_activated:
                self.log(f"{Fore.RED}Gagal mengaktivasi referral, lanjut ke berikutnya."); continue
            
            await asyncio.sleep(random.uniform(1, 2))
            referee_id_token = await self.process_secure_token(referee_pk, referee_address, proxy)
            if not referee_id_token:
                self.log(f"{Fore.RED}Gagal login, lanjut ke berikutnya."); continue
            
            self.save_generated_account(referee_pk, referee_address)
            await asyncio.sleep(random.uniform(2, 4))
            
            await self.run_first_interaction(referee_id_token, referee_address, proxy)
            
            self.log(f"Jeda {30} detik sebelum membuat akun berikutnya...")
            await asyncio.sleep(30)

        self.log(f"{Fore.CYAN}{'='*68}{Style.RESET_ALL}")
        self.log(f"{Fore.GREEN+Style.BRIGHT}PROSES SELESAI. Silakan cek statistik referral Anda di website setelah beberapa saat.")

if __name__ == "__main__":
    try:
        bot = BitQuant()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED+Style.BRIGHT}Proses dihentikan oleh pengguna.")