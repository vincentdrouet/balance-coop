import axios from 'axios';
import serverUrl from './url';

function print(product, weight, cut) {
  return axios({
    method: 'post',
    url: `${serverUrl()}/print_label`,
    data: { product, weight, cut },
  });
}

export default print;
