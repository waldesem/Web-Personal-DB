import { defineStore } from 'pinia'
import { ref } from 'vue';
import { authStore } from '@/store/token';
import { server } from '@/share/utilities';

export const fileManagerStore = defineStore('fileManagerStore', () => {

  const storeAuth = authStore();

  const fileManager = ref({
    path: Array<string>(),
    folders: Array<string>(),
    files: Array<string>(),
    action: '',
    select: false,
    selected: Array<string>(),
    copied: Array<string>(),
  });

  const modalValue = ref("");
  const fileItem = ref("");

  async function getFoldersFiles() {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/manager`);
      const { path, dirs, files }= response.data;
      
      assignValue(path, dirs, files);
      clearValue();

    } catch (error) {
      console.error(error);
    }
  };

  async function openFolder(item: string) {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/open`, {
        'path': fileManager.value.path,
        'item': item
      });
      const { path, dirs, files } = response.data;
      
      assignValue(path, dirs, files);

    } catch (error) {
      console.error(error);
    }
  };

  async function openParent() {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/parent`, {
        'path': fileManager.value.path
      });
      const { path, dirs, files } = response.data;
      
      assignValue(path, dirs, files);

    } catch (error) {
      console.error(error);
    }
  };


  async function openFile(file: string) {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/download`, {
        'path': fileManager.value.path,
        'item': file
      }, { responseType: 'blob' });
      
      const fileName = file.split('/').pop();
      const fileExtension = fileName?.split('.').pop();
      
      fileItem.value = window.URL.createObjectURL(new Blob([response.data]));

      const link = document.createElement('a');
      link.href = fileItem.value;
      link.download = `${fileName}.${fileExtension}`;
      
      link.dispatchEvent(new MouseEvent('click'));

    } catch (error) {
      console.error(error);
    }
  };


  async function updateItem() {
    try {
      const response = fileManager.value.action === 'create'
        ? await storeAuth.axiosInstance.post(`${server}/manager/${fileManager.value.action}`, {
          'path': fileManager.value.path,
          })
        : await storeAuth.axiosInstance.post(`${server}/manager/${fileManager.value.action}`, {
          'path': fileManager.value.path,
          'old': fileManager.value.selected[0],
          'new': modalValue.value
        });
      const { path, dirs, files } = response.data;
      
      assignValue(path, dirs, files);
      clearValue();
    
    } catch (error) {
      console.error(error);
    }
  };

  async function copyItem() {
    if (fileManager.value.selected.length === 0) {
      return
    };
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/${fileManager.value.action}`, {
        'path': fileManager.value.path,
        'old': fileManager.value.copied,
        'new': fileManager.value.selected,
      });
      const { path, dirs, files } = response.data;
      
      assignValue(path, dirs, files);
      clearValue();
    
    } catch (error) {
      console.error(error);
    }
  };

  async function deleteItem() {
    if (fileManager.value.selected.length === 0) {
      return
    };
    if (confirm("Вы действительно хотите удалить?")) {
      try {
        const response = await storeAuth.axiosInstance.post(`${server}/manager/delete`, {
          'path': fileManager.value.path,
          'items': fileManager.value.selected
        });
        const { path, dirs, files } = response.data;

        assignValue(path, dirs, files);
        clearValue();
    
      } catch (error) {
        console.error(error);
      }
    }
  };

  function assignValue(path: [], dirs: [], files: []) {
    fileManager.value.path = path;
    fileManager.value.folders = dirs;
    fileManager.value.files = files;
  };

  function clearValue() {
    modalValue.value = "";
    fileManager.value.select = false;
    fileManager.value.selected = [];
    fileManager.value.copied = [];
  };

  return {
    fileManager,
    modalValue,
    fileItem,
    getFoldersFiles,
    openFolder,
    openParent,
    openFile,
    updateItem,
    copyItem,
    deleteItem
  }
});
