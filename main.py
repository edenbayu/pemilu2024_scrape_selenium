from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv


def get_provinces(driver) -> list:
    ENDPOINT = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara'
    driver.get(ENDPOINT)
    
    provinces = []

    # Navigate to the webpage with the table
    # Find the table element
    table = driver.find_element(By.CLASS_NAME, "table")

    # Find all the <a> tags within the table
    province_elements = table.find_elements(By.TAG_NAME, "a")
    for province_element in province_elements:
        province_name = province_element.text
        province_id = province_element.get_attribute('href').split('/')[-1]
        provinces.append({"name": province_name, 
                          "kode": province_id})
    return provinces

def get_cities(driver, prov_id) -> list:
    ENDPOINT = f'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{prov_id}'
    driver.get(ENDPOINT)
    
    cities = []
    # Navigate to the webpage with the table

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, "table")

    # Find all the <a> tags within the table
    cities_elements = table.find_elements(By.TAG_NAME, "a")
    for cities_element in cities_elements:
        cities_name = cities_element.text
        cities_id = cities_element.get_attribute('href').split('/')[-1]
        if cities_name and cities_id:  # Check if both name and id are not empty
            cities.append({"name": cities_name, 
                              "kode": cities_id})
        else:
            continue
    return cities

def get_kecamatan(driver, prov_id, city_id) -> list:
    ENDPOINT = f'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{prov_id}/{city_id}'
    driver.get(ENDPOINT)
    
    kecamatan = []
    # Navigate to the webpage with the table

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, "table")

    # Find all the <a> tags within the table
    kecamatan_elements = table.find_elements(By.TAG_NAME, "a")
    for kecamatan_element in kecamatan_elements:
        kecamatan_name = kecamatan_element.text
        kecamatan_id = kecamatan_element.get_attribute('href').split('/')[-1]
        if kecamatan_name and kecamatan_id:  # Check if both name and id are not empty
            kecamatan.append({"name": kecamatan_name, 
                              "kode": kecamatan_id})
        else:
            continue
    return kecamatan

def get_kelurahan(driver, prov_id, city_id, kecamatan_id) -> list:
    ENDPOINT = f'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{prov_id}/{city_id}/{kecamatan_id}'
    driver.get(ENDPOINT)
    
    kelurahan = []
    # Navigate to the webpage with the table

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, "table")

    # Find all the <a> tags within the table
    kelurahan_elements = table.find_elements(By.TAG_NAME, "a")
    for kelurahan_element in kelurahan_elements:
        kelurahan_name = kelurahan_element.text
        kelurahan_id = kelurahan_element.get_attribute('href').split('/')[-1]
        if kelurahan_name and kelurahan_id:  # Check if both name and id are not empty
            kelurahan.append({"name": kelurahan_name, 
                              "kode": kelurahan_id})
        else:
            continue
    return kelurahan

def get_tps(driver, prov_id, city_id, kecamatan_id, kelurahan_id) -> list:
    ENDPOINT = f'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{prov_id}/{city_id}/{kecamatan_id}/{kelurahan_id}'
    driver.get(ENDPOINT)
    
    tps = []
    # Navigate to the webpage with the table

    # Find the table element
    table = driver.find_element(By.CLASS_NAME, "table")

    # Find all the <a> tags within the table
    tps_elements = table.find_elements(By.TAG_NAME, "a")
    for tps_element in tps_elements:
        tps_name = tps_element.text
        tps_id = tps_element.get_attribute('href').split('/')[-1]
        if tps_name and tps_id:  # Check if both name and id are not empty
            tps.append({"name": tps_name, 
                              "kode": tps_id})
        else:
            continue
    return tps

def get_c1_form_src(driver, prov_id, city_id, kecamatan_id, kelurahan_id, tps_id, fields, data):
    ENDPOINT = f'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{prov_id}/{city_id}/{kecamatan_id}/{kelurahan_id}/{tps_id}'
    driver.get(ENDPOINT)

    image_elements = driver.find_elements(By.XPATH, "//div[@class='col-md-4']//img")
    # Iterate over each image element and extract its src attribute
    for image_element in image_elements:
        src = image_element.get_attribute("src")
        for i, img in enumerate(src, start=1):
            key = f'Form_Hasil-C_{i}'
            fields.append(key)
            data[key] = img

def directory(path: str = './datasets') -> None:
  if not (os.path.exists(path) and os.path.isdir(path)): os.makedirs(path)

def write_csv(path: str = 'data.csv', data: dict = None, fields: list = []) -> None:
    if data is None:
        data = {}
    if not os.path.exists(path):
        with open(path, mode='w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
    else:
        with open(path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(data)

def main():
    driver = webdriver.Chrome()
    directory(path = f'./datasets/')
    provinces = get_provinces(driver)
    for v_provinces in provinces:
        prov_name = v_provinces['name']
        prov_code = v_provinces['kode']

        cities = get_cities(driver, prov_code)
        for v_city in cities:
            city_name = v_city["name"]
            city_code = v_city["kode"]

            kecamatan = get_kecamatan(driver, prov_code, city_code)
            for v_kecamatan in kecamatan:
                kecamatan_name = v_kecamatan["name"]
                kecamatan_code = v_kecamatan["kode"]

                kelurahan = get_kelurahan(driver, prov_code, city_code, kecamatan_code)
                for v_kelurahan in kelurahan:
                    kelurahan_name = v_kelurahan["name"]
                    kelurahan_code = v_kelurahan["kode"]

                    tps = get_tps(driver, prov_code, city_code, kecamatan_code, kelurahan_code)
                    for v_tps in tps:
                        tps_name = v_tps["name"]
                        tps_code = v_tps["kode"]

                        fields = [
                            'Province_ID',
                            'Province_Name',
                            'City_ID',
                            'City_Name',
                            'Kecamatan_ID',
                            'Kecamatan_Name',
                            'Kelurahan_ID',
                            'Kelurahan_Name',
                            'TPS_ID',
                            'TPS_Name']

                        data = {
                            'Province_ID': prov_code,
                            'Province_Name': prov_name,
                            'City_ID': city_code,
                            'City_Name': city_name,
                            'Kecamatan_ID': kecamatan_code,
                            'Kecamatan_Name': kecamatan_name,
                            'Kelurahan_ID': kelurahan_code,
                            'Kelurahan_Name': kelurahan_name,
                            'TPS_ID': tps_code,
                            'TPS_Name': tps_name
                        }

                        write_csv(
                            path = f'./datasets/{prov_name}.csv',
                            fields = fields,
                            data = data
                            )
                        
                        get_c1_form_src(driver, prov_code, city_code, kecamatan_code, kelurahan_code, tps_code, fields=fields, data=data)

if __name__ == '__main__':
    main()