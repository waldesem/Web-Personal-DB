import axios from 'axios';

const url = 'http://localhost:5000';

const response = await axios.get(`${url}/status`);
const resp = response.data;

const roles = {
    admin: 'admin',
    superuser: 'superuser',
    user: 'user',
    api: 'api'
}


const config = {
  appUrl: url,
  status: resp,
  roles: roles
}; 

export default config;