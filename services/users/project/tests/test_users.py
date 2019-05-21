# jservices/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_users(self):
        """
        Asegurar que un nuevo usuario pueda ser
        agregado a la base de datos"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jos',
                    'email': 'josvillegas@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('josvillegas@upeu.edu.pe', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """
        Asegurando de que se produce un error si el objetivo
        JSON esta vacio"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_keys(self):
        """
        Asegurando de que se produce un error si el objetivo JSON no
        tiene un key username."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'josvillegas@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """
        Asegurando de que se produce un error si el correo
        electronico ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jos',
                    'email': 'josvillegas@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'jos',
                    'email': 'josvillegas@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Asegurando que se obtenga un user de forma correcta."""
        user = add_user('jos', 'josvillegas@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('jos', data['data']['username'])
            self.assertIn('josvillegas@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """
        Asegúrese de que se arroje un error si no
        se proporciona una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """
        Asegurando de que se arroje un error si la identificación no existe.
        """
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_user('jos', 'josvillegas@upeu.edu.pe')
        add_user('toshi', 'tofoshi@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('jos', data['data']['users'][0]['username'])
            self.assertIn(
                'josvillegas@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('toshi', data['data']['users'][1]['username'])
            self.assertIn(
                'tofoshi@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando que la ruta principal funcione correctamente cuando no
        hay usuarios añadidos a la base de datos"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No hay usuarios!</p>', response.data)

    def test_main_with_users(self):
        """Asegurando que la ruta principal funcione correctamente cuando no
        hay usuarios añadidos a la base de datos"""
        add_user('jos', 'josvillegas@upeu.edu.pe')
        add_user('toshi', 'tofoshi@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'jos', response.data)
            self.assertIn(b'toshi', response.data)

    def test_main_add_users(self):
        """        Asegurando que un nuevo usuario pueda ser agregado a la db
        mediante un POST request"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='jos', email='josvillegas@upeu.edu.pe'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'jos', response.data)


if __name__ == '__main__':
    unittest.main()
