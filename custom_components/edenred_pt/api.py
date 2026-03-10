
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)


class EdenredClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None  # mantido apenas em memória

    async def _post(self, session, url, payload):
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"Erro POST {resp.status}: {await resp.text()}")
            return await resp.json()

    async def _get(self, session, url):
        headers = {
            "authorization": self.token,
            "accept": "application/json, text/javascript, */*; q=0.01",
            "x-requested-with": "XMLHttpRequest",
        }
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Erro GET {resp.status}: {await resp.text()}")
            return await resp.json()

    async def authenticate(self):
        url = (
            "https://www.myedenred.pt/edenred-customer/v2/authenticate/default"
            "?appVersion=1.0&appType=PORTAL&channel=WEB"
        )

        async with aiohttp.ClientSession() as session:
            result = await self._post(
                session,
                url,
                {"userId": self.email, "password": self.password},
            )

        self.token = result["data"]["token"]
        _LOGGER.debug("Token obtido com sucesso")

    async def get_cards(self):
        if not self.token:
            await self.authenticate()

        url = (
            "https://www.myedenred.pt/edenred-customer/v2/protected/card/list"
            "?appVersion=1.0&appType=PORTAL&channel=WEB"
        )

        async with aiohttp.ClientSession() as session:
            return await self._get(session, url)

    async def get_card_details(self, card_id):
        url = (
            f"https://www.myedenred.pt/edenred-customer/v2/protected/card/{card_id}/accountmovement"
            "?appVersion=1.0&appType=PORTAL&channel=WEB"
        )

        async with aiohttp.ClientSession() as session:
            return await self._get(session, url)
