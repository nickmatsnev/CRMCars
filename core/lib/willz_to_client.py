import json


def convert(willz_json_data):
    client = {}
    client['willz_external_id'] = willz_json_data['id']
    client['created_at'] = willz_json_data['created_at']

    individuals = []

    for drvr in willz_json_data['drivers']:
                if drvr['id'] == willz_json_data['driver_id']:
                    primary = True
                else:
                    primary = False

                individual = {'primary': primary, 'willz_external_id':drvr['id'],'last_name': drvr['lastname']
                    , 'first_name': drvr['firstname'], 'middle_name': drvr['middlename'],
                              'email': drvr['email']
                    , 'phone': drvr['phone'], 'gender': drvr['gender_id'],
                              'birthday': drvr['birthday']}

                images = []
                for img in range(1, 5):
                    new_img_txt = 'image{0}'.format(img)
                    image = {'title': drvr['passport'][new_img_txt],
                                  'url': drvr['passport'][new_img_txt + '_url']}
                    images.append(image)

                passport = {'number': drvr['passport']['number']
                    , 'issued_at': drvr['passport']['issued_at'], 'issued_by': drvr['passport']['issued_by']
                    , 'address_registration': drvr['passport']['address_registration']
                    , 'division_code': drvr['passport']['division_code'],
                                   'birthplace': drvr['passport']['birthplace'], 'images':images}

                individual['passport'] = passport

                lcn_number = drvr['driver_license']['number']
                if lcn_number == "":
                    lcn_number = 0

                images = []
                for img in range(1, 3):
                    new_img_txt = 'image{0}'.format(img)
                    image = {'title': drvr['passport'][new_img_txt],
                             'url': drvr['passport'][new_img_txt + '_url']}
                    images.append(image)

                driver_license = {'number': lcn_number
                    , 'issued_at': drvr['driver_license']['issued_at'], 'images': images}

                individual['driver_license'] = driver_license


                individuals.append(individual)

    client['individuals'] = individuals

    return client

