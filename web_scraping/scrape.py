import requests
from bs4 import BeautifulSoup
import json

url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=ttspT8gPkNrc+uIDiVpveQ=="
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def get_text_by_id(soup, id_):
    tag = soup.find(id=id_)
    return tag.get_text(strip=True) if tag else None

data = {
    "CodigoExterno": get_text_by_id(soup, "lblNumLicitacion"),
    "Nombre": get_text_by_id(soup, "lblFicha1Nombre"),
    "Estado": get_text_by_id(soup, "lblFicha1Estado"),
    "Descripcion": get_text_by_id(soup, "lblFicha1Descripcion"),
    "Comprador": {
        "NombreOrganismo": get_text_by_id(soup, "lnkFicha2Razon"),
        "NombreUnidad": get_text_by_id(soup, "lblFicha2Unidad"),
        "RutUnidad": get_text_by_id(soup, "lblFicha2RUT"),
        "DireccionUnidad": get_text_by_id(soup, "lblFicha2Direccion"),
        "ComunaUnidad": get_text_by_id(soup, "lblFicha2Comuna"),
        "RegionUnidad": get_text_by_id(soup, "lblFicha2Region")
    },
    "Fechas": {
        "FechaCierre": get_text_by_id(soup, "lblFicha3Cierre"),
        "FechaPublicacion": get_text_by_id(soup, "lblFicha3Publicacion"),
        "FechaInicioPreguntas": get_text_by_id(soup, "lblFicha3Inicio"),
        "FechaFinPreguntas": get_text_by_id(soup, "lblFicha3Fin"),
        "FechaPubRespuestas": get_text_by_id(soup, "lblFicha3PublicacionRespuestas"),
        "FechaActoAperturaTecnica": get_text_by_id(soup, "lblFicha3ActoAperturaTecnica"),
        "FechaActoAperturaEconomica": get_text_by_id(soup, "lblFicha3ActoAperturaEconomica"),
        "FechaAdjudicacion": get_text_by_id(soup, "lblFicha3Adjudicacion")
    },
    "Tipo": get_text_by_id(soup, "lblFicha1Tipo"),
    "TipoConvocatoria": get_text_by_id(soup, "lblFicha1Convocatoria"),
    "Moneda": get_text_by_id(soup, "lblFicha1Moneda"),
    "Etapas": get_text_by_id(soup, "lblFicha1Etapas"),
    "TomaRazon": get_text_by_id(soup, "lblFicha1TR"),
    "PublicidadOfertas": get_text_by_id(soup, "lblFicha1Publicidad"),
    "CantidadReclamos": get_text_by_id(soup, "lblFicha2Reclamo"),
    "Productos": [
        {
            "NombreProducto": get_text_by_id(soup, "grvProducto_ctl02_lblProducto"),
            "Cantidad": get_text_by_id(soup, "grvProducto_ctl02_lblCantidad"),
            "UnidadMedida": get_text_by_id(soup, "grvProducto_ctl02_lblUnidad"),
            "CodigoCategoria": get_text_by_id(soup, "grvProducto_ctl02_lblCategoria"),
            "Descripcion": get_text_by_id(soup, "grvProducto_ctl02_lblDescripcion")
        }
        # Puedes agregar más productos cambiando el sufijo ctl02 por ctl03, ctl04, etc.
    ],
    "CriteriosEvaluacion": [
        {
            "NombreCriterio": get_text_by_id(soup, "grvCriterios_ctl02_lblNombreCriterio"),
            "Observaciones": get_text_by_id(soup, "grvCriterios_ctl02_lblObservaciones"),
            "Ponderacion": get_text_by_id(soup, "grvCriterios_ctl02_lblPonderacion")
        }
        # Agrega más criterios cambiando el sufijo ctl02 por ctl03, ctl04, etc.
    ],
    "MontosYDuracion": {
        "Estimacion": get_text_by_id(soup, "lblFicha7Estimacion"),
        "FuenteFinanciamiento": get_text_by_id(soup, "lblFicha7Financiamiento"),
        "ContratoRenovacion": get_text_by_id(soup, "lblFicha7ContratoRenovacion"),
        "Observaciones": get_text_by_id(soup, "lblFicha7Observacion"),
        "PlazosPago": get_text_by_id(soup, "lblFicha7Plazos"),
        "OpcionesPago": get_text_by_id(soup, "lblFicha7Opciones"),
        "NombreResponsablePago": get_text_by_id(soup, "lblFicha7NombreResponsablePago"),
        "EmailResponsablePago": get_text_by_id(soup, "lblFicha7EmailResponsablePago"),
        "Subcontratacion": get_text_by_id(soup, "lblFicha7Subcontratacion")
    },
    "Garantias": [
        {
            "TipoGarantia": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8TituloTipoGarantia"),
            "Beneficiario": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8Beneficiario"),
            "FechaVencimiento": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8FechaVencimiento"),
            "Monto": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8Monto"),
            "TipoMoneda": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8TipoMoneda"),
            "Descripcion": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8Descripcion"),
            "Glosa": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8Glosa"),
            "Restitucion": get_text_by_id(soup, "grvGarantias_ctl02_lblFicha8Restitucion")
        }
        # Agrega más garantías cambiando el sufijo ctl02 por ctl03, ctl04, etc.
    ]
}

with open("licitacion.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)