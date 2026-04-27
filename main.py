import analysis
import init_database

command = input('have you inittialized database?:\ny for yes\n n for no\nenter:')

if command.lower() == 'y':
    analysis.analyze()
if command.lower() == 'n':
    init_database.initialize()
    analysis.analyze()