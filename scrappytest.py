import sys

from requests_html import HTMLSession

URL_AFINITY2 = "https://www.filmaffinity.com/es/search.php?stext="


def getimagenasync(titulo):  # cambiar por ponerlo directo a la url
    try:

        # print("LLamado")
        sesion = HTMLSession()
        apiafinity = sesion.get(URL_AFINITY2 + titulo)
        apiafinity.html.render()

        # print(titulo)
        # mc-poster
        datos = apiafinity.html.find(".mc-poster > a > img")
        if datos:
            imagen = datos[0].attrs["src"]
            if imagen is not None:
                print(imagen)
                return True
        else:
            datos = apiafinity.html.find("#movie-main-image-container")
            if datos:
                imagen = list(datos[0].absolute_links)[0]
                if imagen is not None:
                    print(imagen)
                    return True
            else:
                # affinity busca por google con delay de 200ms
                datos = apiafinity.html.find("img.gs-image")
                if datos:
                    imagen = datos[0].attrs["src"]
                    print(imagen)
                    return True
        print("None")
        return False
    except ConnectionResetError:
        print("None")
        return False


if __name__ == '__main__':
    titulin = str(sys.argv[1])
    # print(titulin)
    getimagenasync(titulin)

# resultado = getimagenasync("Joker")
