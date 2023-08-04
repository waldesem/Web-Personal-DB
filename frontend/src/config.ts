import axios from 'axios';

const url = 'http://localhost:5000';

const response = await axios.get(`${url}/classify`);
const [statuses, roles, conclusions, decisions, categories] = response.data;

const config = {
  appUrl: url,
  status: statuses,
  roles: roles,
  conclusions: conclusions,
  decisions: decisions,
  categories: categories,
}; 

export default config;