import axios from 'axios';

const url = 'http://localhost:5000';

const response = await axios.get(`${url}/status`);
const resp = response.data;

const config = {
  appUrl: url,
  status: resp
}; 

export default config;