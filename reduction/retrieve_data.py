from astroquery.alma import Alma

alma = Alma()
alma.cache_location = Alma.cache_location = '.'
alma.login('keflavich')

results = alma.query(payload=dict(project_code='2016.1.00550.S'), public=False, cache=False)

all_data = alma.retrieve_data_from_uid(results['Member ous id'])
