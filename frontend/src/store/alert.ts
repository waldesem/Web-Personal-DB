import { defineStore } from 'pinia';

export const alertStore = defineStore('alertStore', () => {

  const alertMessage = ({
    attr: '',
    text: '',
    show: false,
    setAlert: function(attr: string = '', text: string = '') {
      this.show = true;
      Object.assign(this, {
        attr: attr,
        text: text
      });
      setTimeout(() => {
        this.show = false;
      }, 10000);
    }
  });
  return { 
    alertMessage 
  }
});

