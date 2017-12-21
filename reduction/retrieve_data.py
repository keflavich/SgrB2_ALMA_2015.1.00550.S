from astroquery.alma import Alma

alma = Alma()
alma.cache_location = Alma.cache_location = '.'
alma.login('keflavich')

results = Alma.query(payload=dict(project_code='2016.1.00550.S'), public=False, cache=False)

band3 = results['Band'] == 3
band6 = results['Band'] == 6

alma.retrieve_data_from_uid(results['Member ous id'][band3])
alma.retrieve_data_from_uid(results['Member ous id'][band6])
