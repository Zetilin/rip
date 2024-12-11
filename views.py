from django.shortcuts import render

reactors = [
    {
        "id": 1,
        "name": "ЭГП-6",
        "description": "ЭГП-6 — энергетический графито-водный гетерогенный реактор канального типа на тепловых нейтронах с естественной циркуляцией, реализующий схему прямого цикла. Его прототипом являются реакторные установки АМ и АМБ.",
        "fuel": "вода",
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "АМБ-200",
        "description": "АМБ-200 — это тип маломощного ядерного реактора, который разрабатывается в России. Этот реактор предназначен для автономного создания тепловой и электрической энергии и может быть использован в различных областях, включая удалённые районы, где нет доступа к централизованным источникам электроэнергии.",
        "fuel": "диоксид урана",
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "РБМК-1000",
        "description": "РБМК-1000 — это тип ядерного реактора, разработанного и построенного в СССР. Он был создан в 1960-х годах и предназначен для производства электроэнергии, а также для выработки изотопов, используемых в медицине и промышленности.",
        "fuel": "двуокись урана",
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "ВВЭР-1000",
        "description": "ВВЭР-1000 — это тип российского ядерного реактора, который был разработан в 1970-х годах и стал одним из наиболее распространённых типов реакторов в мире. ВВЭР-1000 предназначен для выработки электроэнергии и используется на многих атомных электростанциях.",
        "fuel": "вода",
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "АМБ-100",
        "description": "АМБ-100 — это тип маломощного ядерного реактора, который разрабатывается в России. Этот реактор предназначен для автономного создания тепловой и электрической энергии и может быть использован в различных областях, включая удалённые районы, где нет доступа к централизованным источникам электроэнергии.",
        "fuel": "диоксид урана",
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "ЭГП-12",
        "description": "ЭГП-12 — энергетический графито-водный гетерогенный реактор канального типа на тепловых нейтронах с естественной циркуляцией, реализующий схему прямого цикла. Его прототипом являются реакторные установки АМ и АМБ.",
        "fuel": "двуокись урана",
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_station = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "name": "Белоярская АЭС",
    "location": "Филиал АО «Концерн Росэнергоатом» «Белоярская атомная станция» расположен в Свердловской области в 40 км к востоку от города Екатеринбурга на левом берегу Белоярского водохранилища, образованного на реке Пышма при строительстве первой очереди Белоярской АЭС",
    "year": 1962,
    "reactors": [
        {
            "id": 1,
            "value": 80
        },
        {
            "id": 2,
            "value": 65
        },
        {
            "id": 3,
            "value": 50
        }
    ]
}


def getReactorById(reactor_id):
    for reactor in reactors:
        if reactor["id"] == reactor_id:
            return reactor


def getReactors():
    return reactors


def searchReactors(reactor_name):
    res = []

    for reactor in reactors:
        if reactor_name.lower() in reactor["name"].lower():
            res.append(reactor)

    return res


def getDraftStation():
    return draft_station


def getStationById(station_id):
    return draft_station


def index(request):
    reactor_name = request.GET.get("reactor_name", "")
    reactors = searchReactors(reactor_name) if reactor_name else getReactors()
    draft_station = getDraftStation()

    context = {
        "reactors": reactors,
        "reactor_name": reactor_name,
        "reactors_count": len(draft_station["reactors"]),
        "draft_station": draft_station
    }

    return render(request, "reactors_page.html", context)


def reactor(request, reactor_id):
    context = {
        "id": reactor_id,
        "reactor": getReactorById(reactor_id),
    }

    return render(request, "reactor_page.html", context)


def station(request, station_id):
    station = getStationById(station_id)
    reactors = [
        {**getReactorById(reactor["id"]), "value": reactor["value"]}
        for reactor in station["reactors"]
    ]

    context = {
        "station": station,
        "reactors": reactors
    }

    return render(request, "station_page.html", context)
