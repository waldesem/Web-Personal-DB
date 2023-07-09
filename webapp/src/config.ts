const appUrl = 'http://localhost:5000';
const token = localStorage.getItem('jwt_token');

const config = {
  appUrl: appUrl,
  token: token
};

export default config;