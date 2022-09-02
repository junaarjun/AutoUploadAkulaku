import os
import urllib.request
from time import sleep, strftime
import autoit
import pandas as pd
import shutil
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


def openBrowser():
    global driver
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.maximize_window()
    driver.get('https://ec-vendor.akulaku.com/ec-vendor/user/login')


def login():
    elem_text_login = '//div[contains(text(), "Login")]'
    elem_email = '//input[@id="login_email"]'
    elem_passwoord = '//input[@id="login_pwd"]'
    elem_btn_login = '//span[contains(text(), "Login")]'
    if xpath_check(elem_text_login):
        xpath_type(elem_email, email)
        xpath_type(elem_passwoord, password)
        xpath_el(elem_btn_login)
    else:
        print('Halaman Login Belum Terbuka')


def tambahProduk():
    elem_seller_page = '//*[contains(text(), "Seller Center")]'
    elem_alert = '//div[@id="rcDialogTitle0"]'
    elem_btn_close = '//button[@class="ant-modal-close"]'

    elem_pengaturan_produk = '//a[contains(text(), "Pengaturan Produk")]'
    elem_tambahkan_produk = '//a[contains(text(), "Tambahkan produk")]'

    def klikTambahProduk():
        if xpath_check(elem_tambahkan_produk):
            xpath_el(elem_tambahkan_produk)
        else:
            if xpath_check(elem_pengaturan_produk):
                xpath_el(elem_pengaturan_produk)
                xpath_el(elem_tambahkan_produk)
            else:
                print('Tidak dapat menemukan Element Pengaturan Produk')

    if xpath_check(elem_seller_page):
        if xpath_check(elem_alert):
            xpath_el(elem_btn_close)
            klikTambahProduk()
        else:
            klikTambahProduk()
    else:
        print('Halaman Seller Center Belum Terbuka')


def pilihKategori():
    sleep(1)
    elem_check = '//label[contains(text(), "Judul produk")]'
    elem_input_judul1 = '(//input[@class="ant-input"])[1]'
    elem_kategori1 = f'//p[contains(text(), "{kategori1}")]'
    elem_kategori2 = f'//p[contains(text(), "{kategori2}")]'
    elem_btn_next = '//*[contains(text(), "Selanjutnya, Terbitkan produk")]'

    if xpath_check(elem_check):
        xpath_type(elem_input_judul1, judul_produk)
    else:
        print('tidak')

    xpath_el(elem_kategori1)
    xpath_el(elem_kategori2)
    xpath_el(elem_btn_next)


def inputInfoDasar():
    elem_info_dasar = '//div[@class="ant-tabs-tab ant-tabs-tab-active"]'
    elem_input_judul2 = '//*[@id="name"]'
    elem_input_merek = '//input[@id="brandId"]'

    while driver.find_element(by=By.XPATH, value=elem_info_dasar).text != 'Informasi dasar':
        scrollUp()

    value = driver.find_element_by_xpath(elem_input_judul2).get_attribute('value')
    if value == '':
        xpath_type(elem_input_judul2, judul_produk)
    elif value == judul_produk:
        pass

    merek = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, elem_input_merek)))
    sleep(1)
    merek.send_keys(merek_produk)
    sleep(1)
    merek.send_keys(Keys.DOWN)
    sleep(1)
    merek.send_keys(Keys.ENTER)
    sleep(1)


def inputSpesifikasi():
    elem_tambah_spek1 = '//span[contains(text(), "Tambahkan spesifikasi (1/3)")]'
    elem_cb1 = '//input[@type="checkbox"]'
    elem_nama_spek1 = '//input[@placeholder="Masukkan nama spesifikasi, contoh: Warna, dll"]'
    elem_tambah_opsi1 = '//span[contains(text(), "Tambahkan pilihan")]'

    # spesifikasi 1
    if spek1:
        if xpath_check(elem_tambah_spek1):
            # klik tambah spesifikasi
            xpath_el(elem_tambah_spek1)

            # Fokuskan view
            elem_info_penj = '//div[contains(text(), "Informasi penjualan")]'
            target = driver.find_element_by_xpath(elem_info_penj)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # klik checkbox tambah gambar
            xpath_el(elem_cb1)

            # ketik nama spesifikasi produk 1
            xpath_type(elem_nama_spek1, spesifikasi1)

            # Fokuskan view
            target = '//div[contains(text(), "Informasi penjualan")]'
            target = driver.find_element_by_xpath(target)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # input opsi1
            elem_opsi1 = xpath_all('//input[@placeholder="Masukkan nama pilihan, contoh: Merah, dll"]')
            elem_opsi1[0].send_keys(spek1[0])

            # Fokuskan view
            target = '//div[contains(text(), "Spesifikasi 1")]'
            target = driver.find_element_by_xpath(target)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # input opsi spesifikasi 1
            for i in range(len(spek1) - 1):
                try:
                    xpath_el(elem_tambah_opsi1)
                except:
                    scrollDown()
                    xpath_el(elem_tambah_opsi1)
                    pass
                sleep(0.5)
                elem_opsi1 = xpath_all('//input[@placeholder="Masukkan nama pilihan, contoh: Merah, dll"]')
                elem_opsi1[-1].send_keys(spek1[i + 1])
                sleep(0.5)

    elem_tambah_spek2 = '//span[contains(text(), "Tambahkan spesifikasi (2/3)")]'
    elem_nama_spek2 = '//input[@placeholder="Masukkan nama spesifikasi, contoh: Warna, dll"]'

    # spesifikasi 2
    if spek2:
        if xpath_check(elem_tambah_spek2):
            # klik tambah spesifikasi
            try:
                xpath_el(elem_tambah_spek2)
            except:
                try:
                    scrollDown()
                    xpath_el(elem_tambah_spek2)
                except:
                    scrollDown()
                    xpath_el(elem_tambah_spek2)

            # Fokuskan view
            elem_info_penj = '//div[contains(text(), "Informasi penjualan")]'
            target = driver.find_element_by_xpath(elem_info_penj)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # ketik nama spesifikasi produk 1
            target = xpath_all(elem_nama_spek2)
            target[-1].send_keys(spesifikasi2)

            # Fokuskan view
            target = '//span[contains(text(), "Tambahkan pilihan")]'
            target = driver.find_element_by_xpath(target)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # input opsi2
            elem_opsi2 = xpath_all('//input[@placeholder="Masukkan nama pilihan, contoh: Merah, dll"]')
            elem_opsi2[-1].send_keys(spek2[0])

            # Fokuskan view
            target = '//div[contains(text(), "Spesifikasi 2")]'
            target = driver.find_element_by_xpath(target)
            driver.execute_script('arguments[0].scrollIntoView();', target)

            # input opsi spesifikasi 2
            elem_tambah_opsi2 = xpath_all('//span[contains(text(), "Tambahkan pilihan")]')
            for i in range(len(spek2) - 1):
                try:
                    elem_tambah_opsi2[-1].click()
                except:
                    try:
                        scrollDown()
                        elem_tambah_opsi2[-1].click()
                    except:
                        try:
                            scrollDown()
                            elem_tambah_opsi2[-1].click()
                        except:
                            scrollDown()
                            elem_tambah_opsi2[-1].click()
                            pass
                sleep(0.5)
                elem_opsi1 = xpath_all('//input[@placeholder="Masukkan nama pilihan, contoh: Merah, dll"]')
                elem_opsi1[-1].send_keys(spek2[i + 1])
                sleep(0.5)


def inputInfoSpesifikasi():
    def input(nums=0, i1=0, i2=0):
        # harga
        idType(f'skus_{nums}_originalPrice', harga[i1][i2])
        sleep(0.2)
        # jumlah
        idType(f'skus_{nums}_stock', stok[i1][i2])
        sleep(0.2)
        # sk
        idType(f'skus_{nums}_goodsInfos', sku[i1][i2])
        sleep(0.2)

    sleep(1)
    num = 0
    if len(spek1) == 0:
        input()
    else:
        for idx1, x in enumerate(spek1):
            if len(spek2) == 0:
                input(num, idx1, 0)
                num += 1
            else:
                for idx2, y in enumerate(spek2):
                    input(num, idx1, idx2)
                    num += 1


def inputGambardanDesk():
    elem_gbr = '//*[contains(text(), "Gambar utama")]'

    try:
        driver.find_element(by=By.XPATH, value=elem_gbr).click()
    except:
        scrollDown()

    elem_upload = driver.find_elements(by=By.XPATH, value='//div[@class="product-upload-item"]')

    # upload gambar
    idx = 0
    while idx < len(list_gbr):
        sleep(2)
        elem_upload[idx].click()
        sleep(2)
        uploadImg(list_gbr[idx])
        sleep(3)
        try:
            driver.find_element_by_xpath(f'(//div[@class="product-upload-item"])[{idx + 1}]/div/img')
            idx += 1
        except:
            idx -= 1
            pass

    # Fokuskan view
    target = '//span[contains(text(), "Gambar utama")]'
    target = driver.find_element_by_xpath(target)
    driver.execute_script('arguments[0].scrollIntoView();', target)

    # input deskripsi
    if type(deskripsi) == str:
        elem_kalimat = '//span[contains(text(), "Kalimat")]'
        elem_info = '//textarea[@rows="3"]'
        elem_konfirm = '//*[contains(text(), "Konfirmasi")]'

        xpath_el(elem_kalimat)
        xpath_type(elem_info, deskripsi)
        xpath_el(elem_konfirm)


def inputInfoPengiriman():
    elem_send = '//div[@class="ant-tabs-tab ant-tabs-tab-active"]'
    while driver.find_element(by=By.XPATH, value=elem_send).text != 'Informasi pengiriman':
        scrollDown()

    elem_send = driver.find_elements(by=By.XPATH, value='//input[@placeholder="Masukkan"]')
    for idx, elem in enumerate(elem_send[-4:]):
        sleep(1)
        value = list(info_pengiriman.values())[idx]
        elem.send_keys(str(value))
        sleep(1)


def submit():
    xpath_el('//span[contains(text(), "Kirim dan terbitkan")]')
    sleep(5)


def nextProduk():
    body = driver.find_element(by=By.XPATH, value='//*[contains(text(), "Rumah")]')
    body.click()


def xpath_type(el, mount):
    sleep(0.5)
    return wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)


def xpath_el(el):
    element_all = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, el)))
    sleep(0.5)
    return element_all.click()


def xpath_check(el, sec=10):
    sleep(0.5)
    try:
        wait(driver, sec).until(EC.presence_of_all_elements_located((By.XPATH, el)))
        return True
    except:
        return False


def xpath_all(el):
    sleep(0.5)
    return wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, el)))


def idType(el, mount):
    return wait(driver, 10).until(EC.presence_of_element_located((By.ID, el))).send_keys(mount)


def scrollDown():
    body = driver.find_element_by_tag_name('body')
    body.click()
    body.send_keys(Keys.DOWN)
    body.send_keys(Keys.DOWN)
    body.send_keys(Keys.DOWN)
    sleep(1)


def scrollUp():
    body = driver.find_element_by_tag_name('body')
    body.click()
    body.send_keys(Keys.UP)
    body.send_keys(Keys.UP)
    body.send_keys(Keys.UP)
    sleep(1)


def checkElementClickable(el):
    sleep(0.5)
    try:
        wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, el))).click()
        return False
    except:
        return True


def downloadGambar(url, file_name, product):
    roots = os.getcwd()
    path_gambar = os.path.join(roots, 'Gambar')
    path_product = os.path.join(path_gambar, product)
    fn = os.path.join(path_product, f'{file_name}.jpg')
    if os.path.exists(path_product):
        pass
    else:
        os.makedirs(path_product)
    urllib.request.urlretrieve(url, fn)
    return fn


def uploadImg(path):
    sleep(1)
    autoit.win_wait_active("Open")
    sleep(1)
    autoit.control_send("Open", "Edit1", str(path))
    sleep(1)
    autoit.control_send("Open", "Edit1", "{ENTER}")
    sleep(2)


def uploadProduk(produk):
    print(f"[{strftime('%d-%m-%y %X')}] ->-> Menambah Produk {produk}")
    tambahProduk()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Memilih Kategori")
    pilihKategori()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Input Informasi Dasar")
    inputInfoDasar()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Input Spesifikasi")
    inputSpesifikasi()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Input Info Spesifikasi")
    inputInfoSpesifikasi()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Input Gambar dan Deskripsi")
    inputGambardanDesk()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Input Informasi Pengiriman")
    inputInfoPengiriman()

    print(f"[{strftime('%d-%m-%y %X')}] ->-> Submit Produk")
    submit()


def clearFolder():
    roots = os.path.join(os.getcwd(), 'Gambar')
    shutil.rmtree(roots)


def main():
    global judul_produk, kategori1, kategori2, merek_produk, spesifikasi1, opsi_spek1, spek1, spesifikasi2, opsi_spek2
    global spek2, harga, sku, stok, gambar1, gambar2, gambar3, gambar4, gambar5, gambar6, gambar7, gambar8, deskripsi
    global info_pengiriman, list_gbr

    data = pd.read_excel('data.xlsx')
    cols = data.columns
    print(f"[{strftime('%d-%m-%y %X')}] -> Data terdeteksi!")

    openBrowser()
    print(f"[{strftime('%d-%m-%y %X')}] -> Membuka browser")

    login()
    print(f"[{strftime('%d-%m-%y %X')}] -> Login")

    for index in range(len(data)):
            produk = f'{index + 1}/{len(data)}'
            row = data.iloc[index]
            judul_produk = row[cols[0]]
            kategori1 = row[cols[1]]
            kategori2 = row[cols[2]]
            merek_produk = row[cols[3]]
            spesifikasi1 = row[cols[4]]
            opsi_spek1 = row[cols[5]]
            spesifikasi2 = row[cols[6]]
            opsi_spek2 = row[cols[7]]
            hrg = row[cols[8:18]]
            st = row[cols[18:28]]
            sk = row[cols[28:38]]
            gambar1 = row[cols[38]]
            gambar2 = row[cols[39]]
            gambar3 = row[cols[40]]
            gambar4 = row[cols[41]]
            gambar5 = row[cols[42]]
            gambar6 = row[cols[43]]
            gambar7 = row[cols[44]]
            gambar8 = row[cols[45]]
            deskripsi = row[cols[46]]
            info = row[cols[47:]]
            if type(opsi_spek1) == str:
                spek1 = str(opsi_spek1).replace(" ", "")
                spek1 = spek1.split('|')
            elif type(opsi_spek1) != np.float64 or type(opsi_spek1) != float:
                spek1 = []
            if type(opsi_spek2) == str:
                spek2 = str(opsi_spek2).replace(" ", "")
                spek2 = spek2.split('|')
            elif type(opsi_spek2) != np.float64 or type(opsi_spek2) != float:
                spek2 = []


            harga = []
            sku = []
            stok = []
            if len(spek1) == 0:
                harga = [[str(hrg[0])]]
                sku = [[str(sk[0])]]
                stok = [[str(st[0])]]
            else:
                for a in range(len(spek1)):
                    if type(str(hrg[a])) == str:
                        hrg1 = str(hrg[a]).split('|')
                        harga.append(hrg1)
                    if type(sk[a]) == str:
                        sk1 = sk[a].split('|')
                        sku.append(sk1)
                    if type(str(st[a])) == str:
                        st1 = str(st[a]).split('|')
                        stok.append(st1)

            list_gbr = []
            for i in range(8):
                if type(globals()[f'gambar{i + 1}']) == str:
                    path = downloadGambar(globals()[f'gambar{i + 1}'], f'Gambar-{i + 1}', f'Produk-{index + 1}')
                    list_gbr.append(path)
                else:
                    pass

            info_pengiriman = {
                'berat': info[0],
                'panjang': info[1],
                'lebar': info[2],
                'tinggi': info[3]
            }

            print(f"[{strftime('%d-%m-%y %X')}] -> Mulai Upload produk {index + 1}/{len(data)}")
            uploadProduk(produk)
            print(f"[{strftime('%d-%m-%y %X')}] -> Produk {index + 1}/{len(data)} Berhasil "
                  f"Terpublish\n###############################################\n")
            nextProduk()


if __name__ == '__main__':
    print(f"[{strftime('%d-%m-%y %X')}] ----- Mulai Auto Upload -----")
    file_akun = "akun_akulaku.txt"
    myfile_akun = open(f"{os.getcwd()}\\{file_akun}", "r")
    akun = myfile_akun.read()
    email, password = akun.split("|")
    print(f"[{strftime('%d-%m-%y %X')}] -> Akun terdeteksi")
    main()
    print(f"[{strftime('%d-%m-%y %X')}] ----- Auto Upload Selesai -----")
    ask = input('Close Browser? (y/n)')
    if ask == 'y':
        clearFolder()
        driver.quit()

