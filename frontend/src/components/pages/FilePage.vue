<script setup lang="ts">

import { ref } from 'vue';
import { onBeforeMount, defineAsyncComponent } from 'vue';
import { authStore } from '@/store/token';
import { server } from '@/utilities/utils';

const ModalWin = defineAsyncComponent(() => import('@components/layouts/ModalWin.vue'));
const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeAuth = authStore();

const props = defineProps({
  path: {
    type: Array<string>,
    required: true
  }
});

onBeforeMount(() => {
  fileManager.value.path = props.path.slice(0, -1);
  fileManager.value.openFolder(props.path[-1]);  
});
  
  const fileManager = ref({
    path: Array<string>(),
    folders: Array<string>(),
    files: Array<string>(),
    action: '',
    select: false,
    selected: Array<string>(),
    copied: Array<string>(),
    form: '',
    item: '',
    getFoldersFiles: async function () {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/manager`);
      const { path, dirs, files }= response.data;
      this.assignValue(path, dirs, files);
      this.clearValue();
    } catch (error) {
      console.error(error);
    }
  },

  openFolder: async function (item: string) {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/open`, {
        'path': this.path,
        'item': item
      });
      const { path, dirs, files } = response.data;
      this.assignValue(path, dirs, files);
    } catch (error) {
      console.error(error);
    }
  }, 

  openParent: async function () {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/parent`, {
        'path': this.path
      });
      const { path, dirs, files } = response.data;
      this.assignValue(path, dirs, files);
    } catch (error) {
      console.error(error);
    }
  },

  openFile: async function (file: string) {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/manager/download`, {
        'path': this.path,
        'item': file
      }, { responseType: 'blob' });
      
      const fileName = file.split('/').pop();
      const fileExtension = fileName?.split('.').pop();
      
      this.item = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = this.item;
      link.download = `${fileName}.${fileExtension}`;
      link.dispatchEvent(new MouseEvent('click'));
    } catch (error) {
      console.error(error);
    }
  },

  updateItem: async function () {
    try {
      const response = this.action === 'create'
        ? await storeAuth.axiosInstance.post(`${server}/manager/${this.action}`, {
          'path': this.path,
          })
        : await storeAuth.axiosInstance.post(`${server}/manager/${this.action}`, {
          'path': this.path,
          'old': this.selected[0],
          'new': this.form
        });
      const { path, dirs, files } = response.data;
      this.assignValue(path, dirs, files);
      this.clearValue();
    } catch (error) {
      console.error(error);
    }
  },

  copyItem: async function () {
    if (this.selected.length) {
      try {
        const response = await storeAuth.axiosInstance.post(`${server}/manager/${this.action}`, {
          'path': this.path,
          'old': this.copied,
          'new': this.selected,
        });
        const { path, dirs, files } = response.data;
        this.assignValue(path, dirs, files);
        this.clearValue();
      } catch (error) {
        console.error(error);
      }
    }
  },

  deleteItem: async function () {
    if (this.selected.length) {
      if (confirm("Вы действительно хотите удалить?")) {
        try {
          const response = await storeAuth.axiosInstance.post(`${server}/manager/delete`, {
            'path': this.path,
            'items': this.selected
          });
          const { path, dirs, files } = response.data;
          this.assignValue(path, dirs, files);
          this.clearValue();
        } catch (error) {
          console.error(error);
        }
      }
    }
  },

  assignValue: function (path: [], dirs: [], files: []) {
    this.path = path;
    this.folders = dirs;
    this.files = files;
  },

  clearValue: function () {
    this.form = "";
    this.select = false;
    this.selected = [];
    this.copied = [];
  }
  });

</script>

<template>
  <div class="container py-3">
    
    <HeaderDiv page-header="Файловый менеджер" />

    <div class="border border-primary p-5" id="fileManager">

      <div class="row border border-primary p-3">
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="fileManager.getFoldersFiles" >
            <i class="bi bi-house" title="Дом"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="fileManager.action = 'create'; 
                    fileManager.updateItem()"
            :disabled="fileManager.select">
            <i class="bi bi-plus-square" title="Создать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="fileManager.select = !fileManager.select;
                  fileManager.selected = []">
            <i class="bi bi-check-square" title="Выбрать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="fileManager.action = 'copy'; 
                          fileManager.copied = fileManager.path;
                          fileManager.select = false"
                  :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-clipboard" title="Копировать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="fileManager.action = 'сut'; 
                          fileManager.copied = fileManager.path;
                          fileManager.select = false"
                  :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-scissors" title="Вырезать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="fileManager.select || fileManager.selected.length === 0"
                  @click="fileManager.copyItem">
            <i class="bi bi-clipboard-fill" title="Вставить"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
                  @click="fileManager.action = 'rename'"
                  :disabled="!fileManager.select || fileManager.selected.length !== 1"
                  data-bs-toggle="modal" data-bs-target="#modalFile">
            <i class="bi bi-pencil" title="Переменовать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="!fileManager.select || fileManager.selected.length === 0"
                  @click="fileManager.deleteItem">
            <i class="bi bi-trash" title="Удалить"></i>
          </button>
        </div>
      </div>
    
      <div class="py-3">
        <nav aria-label="breadcrumb" :disabled="fileManager.select">
          <ol class="breadcrumb">
            <li class="breadcrumb-item active" aria-current="page" 
                v-for="item, idx in fileManager.path" :key="item">
              <a href="#" @click="fileManager.path = fileManager.path.slice(0, idx); 
                                  fileManager.openFolder(item)">
                {{ item }}
              </a>
            </li>
          </ol>
        </nav>
      </div>

      <ul class="list-group">

        <li class="list-group-item" v-if="fileManager.path.length">
          <button type="button" href="#" class="list-group-item list-group-item-action" title="Наверх"
                  @click="fileManager.path = fileManager.path.slice(0, -1); 
                          fileManager.openParent()"
                  :disabled="fileManager.select">
            <i class="bi bi-arrow-90deg-up"></i>
          </button>
        </li>

        <li class="list-group-item" v-for="folder in fileManager.folders" :key="folder">
          <div class="item-wrapper fs-6">
            <input class="form-check-input" type="checkbox" v-if="fileManager.select" 
                  :value="folder" v-model="fileManager.selected">
            &nbsp;
            <button type="button" class="list-group-item list-group-item-action btn btn-light" 
                    @click="fileManager.openFolder(folder)"
                    :disabled="fileManager.select">
              <i class="bi bi-folder"></i>
              {{ folder }}
            </button>
          </div>
        </li>

        <li class="list-group-item" v-for="file in fileManager.files" :key="file">
          <div class="item-wrapper">
            <input class="form-check-input" type="checkbox" v-if="fileManager.select"
                  :value="file" v-model="fileManager.selected">
            &nbsp; &nbsp;
            <button type="button" class="list-group-item list-group-item-action btn btn-light" 
                    @click="fileManager.openFile(file)"
                    :disabled="fileManager.select">
              <i class="bi bi-file"></i>
              {{ file }}
            </button>
          </div>
        </li>

      </ul>
    </div>
    <ModalWin :id="'modalFile'" :title ="'Переменовать'" :size="'modal-md'">
      <form @submit.prevent="fileManager.updateItem" class="form form-check" role="form">
        <div class="row">
          <div class="col">
            <input class="form-control" id="name" maxlength="250" name="name" type="text"
            v-model="fileManager.form">
          </div>
          <div class="col">
            <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">
              Принять
            </button>
          </div>
        </div>
      </form>
    </ModalWin>
  </div>
</template>

<style scoped>

#fileManager {
  height: 75vh;
  max-height: 75vh;
  overflow-y: auto;
}
.list-group-item .item-wrapper {
  display: flex;
  align-items: center;
}
</style>