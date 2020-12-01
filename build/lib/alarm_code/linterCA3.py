import pylint.lint
pylint_opts = ['alarm.py', 'covid.py', 'main.py', 'news.py', 'organise_dictionaries.py', 'time_conversions.py', 'weather.py']
pylint.lint.Run(pylint_opts)
