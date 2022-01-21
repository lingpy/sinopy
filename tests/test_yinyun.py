from sinopy.yinyun import parse_baxter, sixtuple2baxter, baxter2ipa

def test_parse_baxter():

    assert parse_baxter('tsrhangH') == ('tsrh', '', 'ang', 'H')


def test_baxter2ipa():

    assert baxter2ipa('tsrhungX') == "ʦʰuŋ²"


def test_sixtuple2baxter():

    assert "/".join(sixtuple2baxter('臻開三入質影')) == "'//it/R"
