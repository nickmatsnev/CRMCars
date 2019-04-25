import requests


# Получение урла модуля
def get_module_url():
    return "http://api.exbico.ru/se/crm_V4_1"


# импорт сырых данных, физ лицо тут нужно будет, чтобы учитывать параметры конкретного физика
def import_data(credentials_json, individual_json, parsers_data):
    username = "ev@willz.ru"
    password = "Qw123456"

    url = get_module_url()

    request = '''
    <credit_rating>
        <auth>
            <login>{0}</login>
            <password>{1}</password>
        </auth>
        <person>
            <lastname>{2}</lastname>
            <firstname>{3}</firstname>
            <middlename>{4}</middlename>
            <datebirth>{5}</datebirth>
        </person>
        <document>
            <type>21</type>
            <number>{6}</number>
            <series>{7}</series>
            <issuedate>{8}</issuedate>
        </document>
        <loan>
            <loantype>1</loantype>
            <loanamount>150000</loanamount>
            <loanduration>30</loanduration>
        </loan>
        <istest>0</istest>
    </credit_rating>
    '''.format(username, password, individual_json["last_name"], individual_json["first_name"],
               individual_json["middle_name"],
               individual_json["birthday"], individual_json["passport"]["number"][4:],
               individual_json["passport"]["number"][0:4],
               individual_json["passport"]["issued_at"])

    r = requests.post(url, data=request.encode('utf-8'))
    sphere_res = {'result': r.text}
    return sphere_res


# Получение имени модуля
def get_module_name():
    return "NBKI"
