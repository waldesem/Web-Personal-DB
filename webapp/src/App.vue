<template>
  <router-view ></router-view>
</template>

<script>
export default {
  name: 'App',

  async created () {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push({ name: 'login' });
      return;
    }

    const response = await fetch('http://localhost:5000/login', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    const { user } = await response.json();
    user === "Authorized" ? 
      this.$router.push({name: 'index', params: {flag: 'new'}}) : 
      this.$router.push({name: 'login'});
  }
}
</script>
