import axios from 'axios';

const url = 'http://localhost:5000';

const response = await axios.get(`${url}/classify`);
const [statuses, roles, locations, conclusions, decisions, categorys] = response.data;

const config = {
  appUrl: url,
  status: statuses,
  roles: roles,
  locations: locations,
  conclusions: conclusions,
  decisions: decisions,
  categorys: categorys,
}; 

export default config;