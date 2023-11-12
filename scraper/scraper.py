from bs4 import BeautifulSoup
from selenium import webdriver
import time, json

url_list = [
    "https://comococinar.pe/ceviche-de-pescado/",
    "https://comococinar.pe/lomo-saltado/",
    "https://comococinar.pe/papa-a-la-huancaina/",
    "https://comococinar.pe/aji-de-gallina/",
    "https://comococinar.pe/arroz-con-pollo/",
    "https://comococinar.pe/pachamanca-a-la-tierra/",
    "https://comococinar.pe/causa-rellena-de-pollo/",
    "https://comococinar.pe/aguadito-de-pollo/",
    "https://comococinar.pe/rocoto-relleno-arequipeno/",
    "https://comococinar.pe/coctel-de-machu-picchu/",
    "https://comococinar.pe/caldo-de-gallina/",
    "https://comococinar.pe/seco-a-la-nortena/",
    "https://comococinar.pe/picarones/",
    "https://comococinar.pe/estofado-de-pollo/",
    "https://comococinar.pe/arroz-chaufa/",
    "https://comococinar.pe/arroz-con-leche/",
    "https://comococinar.pe/leche-de-tigre/",
    "https://comococinar.pe/pisco-sour/",
    "https://comococinar.pe/menestron/",
    "https://comococinar.pe/pachamanca-a-la-olla/",
    "https://comococinar.pe/aguadito-de-pollo/",
    "https://comococinar.pe/anticucho/",
    "https://comococinar.pe/papa-rellena/",
    "https://comococinar.pe/frejol-canario-con-seco/",
    "https://comococinar.pe/chanfainita-con-mote/",
    "https://comococinar.pe/parihuela-de-mariscos/",
    "https://comococinar.pe/mazamorra-morada/",
    "https://comococinar.pe/pollo-al-horno/",
    "https://comococinar.pe/pollo-al-horno/",
    "https://comococinar.pe/rachi-con-choncholi/",
    "https://comococinar.pe/pollo-al-limon/",
    "https://comococinar.pe/tallarin-saltado-de-pollo/",
    "https://comococinar.pe/caigua-rellena/",
    "https://comococinar.pe/sopa-a-la-minuta/",
    "https://comococinar.pe/pollo-a-la-plancha/",
    "https://comococinar.pe/adobo-de-pollo/",
    "https://comococinar.pe/arroz-a-la-jardinera/",
    "https://comococinar.pe/chicharron-de-pescado/",
    "https://comococinar.pe/arroz-zambito/",
    "https://comococinar.pe/ensalada-rusa/",
    "https://comococinar.pe/mazamorra-de-calabaza/",
    "https://comococinar.pe/sangrecita-de-pollo/",
    "https://comococinar.pe/chocotejas-de-pecanas/",
    "https://comococinar.pe/churros-caseros/",
    "https://comococinar.pe/bistec-a-lo-pobre/",
    "https://comococinar.pe/higado-empanizado/",
    "https://comococinar.pe/sudado-de-pescado/",
    "https://comococinar.pe/chicharron-de-cerdo/",
    "https://comococinar.pe/pollo-al-mani/",
    "https://comococinar.pe/crema-de-rocoto/",
    "https://comococinar.pe/frejol-colado/",
    "https://comococinar.pe/guiso-de-trigo/",
    "https://comococinar.pe/lomito-al-jugo/",
    "https://comococinar.pe/crema-de-zapallo/",
    "https://comococinar.pe/leche-asada/",
    "https://comococinar.pe/chilcano-de-cangrejo/",
    "https://comococinar.pe/zambito-de-quinua/",
    "https://comococinar.pe/escabeche-de-pollo/",
    "https://comococinar.pe/pan-con-relleno/",
    "https://comococinar.pe/chapana/",
    "https://comococinar.pe/humitas-dulces/",
    "https://comococinar.pe/puca-picante/",
    "https://comococinar.pe/aji-de-atun/",
    "https://comococinar.pe/sopa-seca-chinchana/",
    "https://comococinar.pe/tacacho-con-cecina/",
    "https://comococinar.pe/chicharron-de-pota/",
    "https://comococinar.pe/pan-con-pejerrey/",
    "https://comococinar.pe/juane-de-gallina/",
    "https://comococinar.pe/alverjita-partida/",
    "https://comococinar.pe/chancho-con-pina/",
    "https://comococinar.pe/sangria/",
    "https://comococinar.pe/pepian-de-choclo/",
    "https://comococinar.pe/trucha-frita/",
    "https://comococinar.pe/arroz-con-pato/",
    "https://comococinar.pe/pastel-de-choclo/",
    "https://comococinar.pe/guiso-de-garbanzos/",
    "https://comococinar.pe/patita-con-mani/",
    "https://comococinar.pe/pan-con-chicharron/",
    "https://comococinar.pe/empanada-de-carne/",
    "https://comococinar.pe/mazamorra-de-tocosh/",
    "https://comococinar.pe/lentejas-con-pollo/",
    "https://comococinar.pe/cachanga/",
    "https://comococinar.pe/tamales-de-pollo/",
    "https://comococinar.pe/inchicapi-de-gallina/",
    "https://comococinar.pe/budin-de-pan/",
    "https://comococinar.pe/mayonesa-casera/",
    "https://comococinar.pe/pallares-con-seco-de-pollo/",
    "https://comococinar.pe/sopa-de-semola/",
    "https://comococinar.pe/cuy-chactado/",
    "https://comococinar.pe/panqueques-de-avena/",
    "https://comococinar.pe/tortilla-de-coliflor/",
    "https://comococinar.pe/salsa-criolla/",
    "https://comococinar.pe/sopa-de-olluco/",
]

other_urls = [
    "https://comidasperuanas.net/ocopa-arequipena/",
    "https://comidasperuanas.net/picante-de-pollo/",
    "https://comidasperuanas.net/chupe-de-olluco/",
]


def main():
    driver = webdriver.Firefox()

    id = 20000

    json_dict = []

    for url in url_list:
        try:
            id = id + 1
            driver.maximize_window()
            driver.get(url)
            time.sleep(5)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "html.parser")
            name = soup.find("h1", {"class": "entry-title"})
            content = soup.findAll(
                "div", {"class": "elementor-widget-wrap elementor-element-populated"}
            )

            cooktime = (
                content[4]
                .findAll("li")[0]
                .text.replace("Tiempo de preparación: ", "")
                .replace(" minutos", "")
                .replace(" horas", "")
                .replace(" hora", "")
                .split()
            )

            if len(cooktime) >= 2:
                cooktime = (int(cooktime[0]) * 60) + int(cooktime[1])

            servings = (
                content[4]
                .findAll("li")[1]
                .text.replace(" personas", "")
                .replace("Cantidad de comensales: ", "")
            )

            jd = {
                "id": id,
                "name": name.get_text().capitalize(),
                "url": url,
                "image": "",
                "how_to_prepare": [prep.text for prep in content[1].findAll("p")],
                "information": {
                    "cooktime": {
                        "unit": "minutes",
                        "value": cooktime,
                    },
                    "servings": servings,
                },
                "ingredients": [
                    ingredient.text for ingredient in content[6].findAll("li")
                ],
                "preparation": [prep.text for prep in content[8].findAll("li")],
                "recommendations": [rec.text for rec in content[11].findAll("li")],
                "history": [history.text for history in content[13].findAll("p")],
            }

            json_dict.append(jd)

        except IndexError:
            continue

    with open("recipes.json", "w") as file:
        json.dump(json_dict, file, indent=4)
    driver.quit()


if __name__ == "__main__":
    main()
