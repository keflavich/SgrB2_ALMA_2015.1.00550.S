from astroquery.alma import Alma

alma = Alma()
alma.cache_location = Alma.cache_location = '.'
alma.login('keflavich')
alma3 = alma()
alma6 = alma()

results = alma.query(payload=dict(project_code='2016.1.00550.S'), public=False, cache=False)

band3 = results['Band'] == 3
band6 = results['Band'] == 6

all_data = alma.retrieve_data_from_uid(results['Member ous id'])
