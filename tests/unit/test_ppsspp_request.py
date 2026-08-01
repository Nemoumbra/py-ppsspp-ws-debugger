import json

from ppsspp import PPSSPPRequest


def test_serialize():
    request = PPSSPPRequest("name")
    d = json.loads(str(request))
    assert d == {"event": "name"}

    # Nothing new
    request.add()
    d = json.loads(str(request))
    assert d == {"event": "name"}

    request.add(test_str="1", test_int=1, test_float=1.5)
    d = json.loads(str(request))
    assert d == {"event": "name", "test_str": "1", "test_int": 1, "test_float": 1.5}


def test_python_keywords_args():
    request = PPSSPPRequest("name")
    request.add("def", True, value={})
    d = json.loads(str(request))
    assert d == {"event": "name", "def": True, "value": {}}


def test_nullable_arg():
    request = PPSSPPRequest("name")
    request.add(nothing=None)
    d = json.loads(str(request))
    assert d == {"event": "name", "nothing": None}


def test_tickets():
    request = PPSSPPRequest("name")
    kTicket = "sup"

    assert request.get_ticket() is None

    request.set_ticket(kTicket)
    assert request.get_ticket() == kTicket

    d = json.loads(str(request))
    assert d == {"event": "name", "ticket": kTicket}
