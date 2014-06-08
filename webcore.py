import os

import settings
import cloudmanager
import metachains_dtc
import accounts

class WebCore(object):
    def __init__(self):
        self.cloud = cloudmanager.CloudManager(
            settings.DATABASE_PATH,
            settings.STORAGE_PATH,
            settings.STORAGE_SIZE)

        self.coin = metachains_dtc.Datacoin(
            settings.DATACOIN_URL,
            settings.DATACOIN_USERNAME,
            settings.DATACOIN_PASSWORD)

        self.accounts = accounts.create(
            settings.ACCOUNTS_API_ENABLED,
            settings.ACCOUNTS_API_BASE_URL,
            settings.ACCOUNTS_API_KEY)


    def upload_cost(self, file_path):
        return os.path.getsize(file_path) * 4

    def download_cost(self, filehash):
        info = self.cloud.info(filehash)

        if info is None:
            return None

        bytecount = info['filesize']
        if not self.cloud.on_cache(filehash):
            bytecount *= 2

        return bytecount


    def charge_upload(self, token, file_path):
        amount = self.upload_cost(file_path)

        return self.accounts.consume(token, amount)

    def charge_download(self, token, filehash):
        amount = self.download_cost(filehash)

        return self.accounts.consume(token, amount)

    def refund(self, receipt):
        self.accounts.refund(receipt)
