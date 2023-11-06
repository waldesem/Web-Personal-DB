<script setup lang="ts">

import { onBeforeMount, ref } from 'vue';
import { authStore } from '@store/token';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';
import { server } from '@share/utilities';

const storeAuth = authStore();

onBeforeMount(() => {
  getFoldersFiles();  
});

const fileManager = ref({
  path: [],
  folders: [],
  files: [],
  action: '',
  select: false,
  selected: [],
  copied: [],
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

</script>

<template>
  <div class="container py-3">
    
    <HeaderDiv page-header="Файловый менеджер" />

    <div class="border border-primary p-5" id="fileManager">

      <div class="row border border-primary p-3">
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="getFoldersFiles" >
            <i class="bi bi-house" title="Дом"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="fileManager.action = 'create'; updateItem()"
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
                          fileManager.copied = fileManager.selected;
                          fileManager.select = false"
                  :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-clipboard" title="Копировать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="fileManager.action = 'сut'; 
                          fileManager.copied = fileManager.selected;
                          fileManager.select = false"
                  :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-scissors" title="Вырезать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="fileManager.select || fileManager.selected.length === 0"
                  @click="copyItem">
            <i class="bi bi-clipboard-fill" title="Вставить"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
                  @click="fileManager.action = 'rename'"
                  :disabled="!fileManager.select || fileManager.selected.length !== 1"
                  data-bs-toggle="modal" data-bs-target="#modalItem">
            <i class="bi bi-pencil" title="Переменовать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="!fileManager.select || fileManager.selected.length === 0"
                  @click="deleteItem">
            <i class="bi bi-trash" title="Удалить"></i>
          </button>
        </div>
      </div>
    
      <div class="py-3">
        <nav aria-label="breadcrumb" :disabled="fileManager.select">
          <ol class="breadcrumb">
            <li class="breadcrumb-item active" aria-current="page" 
                v-for="item, idx in fileManager.path" :key="item">
              <a href="#" @click="fileManager.path = fileManager.path.slice(0, idx-1); openFolder(item)">
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
                          openFolder(fileManager.path[fileManager.path.length - 1])"
                  :disabled="fileManager.select">
            <i class="bi bi-arrow-90deg-up"></i>
          </button>
        </li>

        <li class="list-group-item" v-for="folder in fileManager.folders" :key="folder">
          <div class="item-wrapper fs-6">
            <input class="form-check-input" type="checkbox" v-if="fileManager.select" 
                  :value="folder" v-model="fileManager.selected">
            &nbsp;
            <button type="button" class="list-group-item list-group-item-action btn btn-light" @click="openFolder(folder)"
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
                    @click="openFile(file)"
                    :disabled="fileManager.select">
              <i class="bi bi-file"></i>
              {{ file }}
            </button>
          </div>
        </li>

      </ul>
    </div>
    
    <div class="modal fade" id="modalItem" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
      <div class="modal-dialog modal-md">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="modalWinLabel">Переменовать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            
            <form @submit.prevent="updateItem" class="form form-check" role="form">
              <div class="row">
                <div class="col">
                  <input class="form-control" id="name" maxlength="250" name="name" type="text"
                  v-model="modalValue">
                </div>
                <div class="col">
                  <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">
                    Принять
                  </button>
                </div>
              </div>
            </form>
      
          </div>
        </div>
      </div>
    </div>

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