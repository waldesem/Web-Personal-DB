import { ref } from 'vue'
import { defineStore } from 'pinia';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { server } from '@share/utilities';


export const tableStore = defineStore('tableStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();

  const tableData = ref({
    table: '',
    item: [],
    search: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false,
    getItem: async function(page: number): Promise<void> {
      this.currentPage = page;
      try {
        const response = await storeAuth.axiosInstance.post(
          `${server}/table/${this.table}/${page}`, {
            'id': this.search
          }
        );
        const [ datas, metadata ] = response.data;
        this.item = datas;
        this.hasNext = metadata.has_next;
        this.hasPrev = metadata.has_prev;
        
      } catch (error) {
        storeAlert.setAlert('alert-warning', error as string);
      }
    },
    deleteItem: async function (idItem: string): Promise<void>{
      if (confirm(`Вы действительно хотите удалить запись?`)) {
        try {
          const response = await storeAuth.axiosInstance.delete(
            `${server}/table/${this.table}/${idItem}`);
          console.log(response.status);
          storeAlert.setAlert('alert-warning', 
                              `Запись ${idItem} из ${this.table} удалена`);
          this.getItem(this.currentPage);
        } catch (error) {
          storeAlert.setAlert('alert-warning', error as string);
        }
      };
    }
  })
  return {
    tableData 
  };
});