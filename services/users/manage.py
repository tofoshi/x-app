# services/users/manage.py
import unittest
import coverage

COV=coverage.coverage(
   branch=True,
   include='project/*',
   omit=[
      'project/tests/*',
      'project/config.py',
   ]
)
COV.start()

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

# nuevo
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# nuevo
@cli.command()
def test():
   """ Ejecutar las pruebas sin covertura de codigo"""
   tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
   result = unittest.TextTestRunner(verbosity=2).run(tests)
   if result.wasSuccessful():
       return 0
   return 1

# nuevo
@cli.command('seed_db')
def seed_db():
   """Sembrado en la base de datos"""
   db.session.add(User(username='jos', email='josvillegas@upeu.edu.pe', password='greaterthaneight'))
   db.session.add(User(username='toshi', email='tofoshi@gmail.com', password='greaterthaneight'))
   db.session.commit()

# nuevo
@cli.command()
def cov():
   """Ejecuta las pruebas unitarias con coverage"""
   tests = unittest.TestLoader().discover('project/tests')
   result = unittest.TextTestRunner(verbosity=2).run(tests)
   if result.wasSuccessful():
      COV.stop()
      COV.save()
      print('Resumen de cobertura')
      COV.report()
      COV.html_report()
      return 0
   sys.exit(result)


if __name__ == '__main__':
    cli()