import os
import argparse
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base URL
BASE_URL = 'https://pemilu2024.kpu.go.id'

# Fungsi untuk mengakses halaman dan melakukan scraping
def scrape_page(url, output_path, queue, ref_queue, driver):
    try:
        # Buka halaman
        driver.get(url)
        print('[LOADED]', url)

        # Cek jika halaman berisi form pindai, jika ya maka scrap datanya
        if 'tps' in output_path.lower() or 'pos' in output_path.lower():
            os.makedirs(output_path, exist_ok=True)

            # Tulis URL ke dalam file link.txt
            with open(os.path.join(output_path, 'link.txt'), 'w') as file:
                file.write(url)

            # Klik tombol 'Form Pindai' jika ada
            btn = driver.find_element(By.XPATH, '//button[@class="btn btn-dark float-end" and text()="Form Pindai"]')
            btn.click()

            # Tunggu sampai elemen yang diharapkan muncul
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card-body div.row div.col-md-4')))
            
            # Scrap gambar-gambar yang ada di halaman
            images = driver.find_elements(By.CSS_SELECTOR, 'div.card-body div.row div.col-md-4 a img')
            for i, image in enumerate(images):
                img_link = image.get_attribute('src')
                ext = img_link.split('.')[-1]
                # Download gambar
                response = requests.get(img_link)
                if response.status_code == 200:
                    with open(os.path.join(output_path, f'{i}.{ext}'), 'wb') as file:
                        file.write(response.content)
                else:
                    print('Failed to download image', img_link)
        else:
            table = driver.find_element(By.CLASS_NAME, "table")
            # Jika halaman bukan form pindai, cari tautan-tautan yang ada di dalam tabel
            items = table.find_elements(By.TAG_NAME, 'a')
            for item in items:
                text = item.text
                next_link = item.get_attribute('href')
                next_path = os.path.join(output_path, text)
                # Jika tautan ditemukan, masukkan ke dalam antrian
                queue.append((next_link, next_path))
                ref_queue.append((next_link, next_path))

    except Exception as e:
        print('Error on', url, ', Path:', output_path)
        print(e)

# Fungsi utama
def main(base_url, start_url, output, timeout, workers, resume):
    # Inisialisasi queue
    queue = []
    
    # Inisialisasi referensi queue
    ref_queue = [(start_url, output)]
    
    # Menambahkan start_url dan output ke dalam queue
    queue.append((start_url, output))

    # Resume sesi sebelumnya jika tersedia
    if resume and os.path.exists('.queue.cache'):
        print('Resuming previous session')
        with open('.queue.cache', 'rb') as file:
            ref_queue = pickle.load(file)

    # Inisialisasi WebDriver
    driver = webdriver.Firefox()

    # Iterasi untuk menjalankan scraping
    while queue:
        # Mendapatkan URL dan output dari queue
        url, output_path = queue.pop(0)
        ref_queue.pop(0)

        # Scrap halaman
        scrape_page(url, output_path, queue, ref_queue, driver)

        # Menyimpan referensi queue
        with open('.queue.cache', 'wb') as file:
            pickle.dump(ref_queue, file)

    # Tutup WebDriver
    driver.quit()

# Jalankan fungsi utama
if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Indonesia Pemilu 2024 Scraper')
    args.add_argument('--start-url', type=str, help=f'Starting url. Base is {BASE_URL}', default=BASE_URL + '/pilpres/hitung-suara')
    args.add_argument('--output', type=str, help='Output directory', default='results')
    args.add_argument('--timeout', type=int, help='Timeout for each request', default=3000)
    args.add_argument('--workers', type=int, help='Total concurrent workers', default=15)
    args.add_argument('--headless', action='store_true', help='Run in headless mode')
    args.add_argument('--resume', action='store_true', help='Resume previous session if available')
    parsed_args = args.parse_args()
    
    print(parsed_args)
    main(BASE_URL, parsed_args.start_url, parsed_args.output, parsed_args.timeout, parsed_args.workers, parsed_args.resume)



