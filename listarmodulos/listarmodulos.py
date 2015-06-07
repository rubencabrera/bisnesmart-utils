#!/usr/bin/env python
# -*- encoding: utf-8 -*-


##############################################################################
#
# OpenERP, Open Source Management Solution
# 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


###############################################################################
#   Author: Rubén Cabrera
#           rcabrera@bisnesmart.com
#           www.bisnesmart.com
#
#   Credits: Created from the useful answer by NUMERIGRAPHE at odoo forum 
#            post: 
# https://www.odoo.com/forum/help-1/question/how-to-uninstall-a-module-from-command-line-36076
###############################################################################
"""List installed modules."""


import xmlrpclib
import argparse
import getpass




parser = argparse.ArgumentParser(description='Listar módulos instalados')
# Connection args
# Argumentos de conexión
parser.add_argument('-d', '--database', help="Use DATABASE as the database name",
                    action='store', metavar='DATABASE', default=getpass.getuser())
parser.add_argument('-u', '--user', help="Use USER as the database user name",
                    action='store', metavar='USER', default='admin')
parser.add_argument('-w', '--password',
                    help="Use PASSWORD as the database password.",
                    action='store', metavar='PASSWORD', default='admin')
parser.add_argument('-s', '--url',
                    help="Point to the web services hosted at URL. Ojo: indicar el http:// ",
                    action='store', metavar='URL')
# Feature args
# Argumentos del módulo
#parser.add_argument('module', help="Uninstall the module MODULE",
#                    action='store', metavar='MODULE')

args = vars(parser.parse_args())
#login(args['url'],args['database'],args['user'],args['password'])



# Log in
ws_common = xmlrpclib.ServerProxy(args['url'] + '/xmlrpc/common')
uid = ws_common.login(args['database'], args['user'], args['password'])
print "Logged in to the common web service."

# Get the object proxy
ws_object = xmlrpclib.ServerProxy(args['url'] + '/xmlrpc/object')
print "Connected to the object web service."
#listarModulos()



# Encontrar la lista de módulos instalados por id
# Esta búsqueda deja fuera otors estados, como el 
# "pendiente de actualizar" que es 'to upgrade'
res_ids = ws_object.execute(
    args['database'], uid, args['password'],
    'ir.module.module', 'search', [('state', '=', 'installed')])
if len(res_ids) < 1:
    raise Exception("Search failed")


# Con la lista de ids, sacar el nombre de los módulos.
lista_modulos = ws_object.execute(args['database'],uid,args['password'],
    'ir.module.module', 'read', res_ids, ['name']
    )
# La web que viene en "website" es inútil a la hora de 
# descargar, es una web de referencia del módulo. 

# lista_modulos es una lista de diccionarios con la pareja
# {id, name}, con lo siguiente nos quedamos sólo con los nombres.

lista_limpia = list()

for element in lista_modulos:
    lista_limpia.append(element['name'])


# Aquí iría bien un menú o una forma de imprimir esto guay:

print lista_limpia


