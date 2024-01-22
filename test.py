import unittest
import requests as r
import json

BASE_URL = 'http://127.0.0.1:7000/'
order_id = -1 
class Test1Ships(unittest.TestCase):
    def test_1_get_all(self):
        path = BASE_URL + 'classes_of_ships'
        ans = r.get(path)
        self.assertEqual(ans.status_code,200)
        self.assertIsNotNone(ans.content)  


    def test_2_post_add_with_data(self):
        path = BASE_URL + r'classes_of_ships/add/'
        payload = {'name':'test',
                    'type':'test',
                    'rang':1,
                    'stuff':100,
                    'project':'test',
                    'description':'test',
                    'status':'Добавлен'}
        ans = r.post(path,data=payload)
        self.assertEqual(ans.status_code,201)
        resp = json.loads(ans.content)
        self.assertIsNotNone(resp.pop('ship_id'))


    def test_3_post_add_without_data(self):
        path = BASE_URL + r'classes_of_ships/add/'
        ans = r.post(path)
        self.assertEqual(ans.status_code,400)

    
class Test2Orders(unittest.TestCase):
    def test_4_add_to_order(self):
        path = BASE_URL + r'classes_of_ships/1/add_to_order/'
        ans = r.post(path)
        self.assertEqual(ans.status_code,204)

    def test_5_approve_forming_order(self):
        path = BASE_URL + 'classes_of_ships'
        ans = r.get(path)
        global order_id
        order_id = json.loads(ans.content)['draft_id']
        path = BASE_URL + r'orders/' + str(order_id) +r'/approve_order/'
        ans = r.put(path)    
        self.assertEqual(ans.status_code,412) 

    def test_6_form_order(self):
        path = BASE_URL + r'orders/form_order/'
        ans = r.put(path)
        self.assertEqual(ans.status_code,204)   
    
    def test_7_approve_active_order(self):
        path = BASE_URL + r'orders/' + str(order_id) +r'/approve_order/'
        ans = r.put(path)    
        self.assertEqual(ans.status_code,204) 
        




if __name__ == '__main__':
    unittest.main()