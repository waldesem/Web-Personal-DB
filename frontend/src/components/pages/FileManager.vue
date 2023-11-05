<script setup lang="ts">

import { computed, onBeforeMount, ref } from 'vue';
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

const modalHeader = computed(() => {
  fileManager.value.action === 'create' ? 'Создать папку' : 'Переименовать';
});

const modalValue = ref("");
const fileItem = ref("");

async function getFoldersFiles() {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/manager`);
    const { path, dirs, files }= response.data;
    fileManager.value.path = path;
    fileManager.value.folders = dirs;
    fileManager.value.files = files;

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
    const { path, dirs, files }= response.data;
    fileManager.value.path = path;
    fileManager.value.folders = dirs;
    fileManager.value.files = files;

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
    
    // Trigger the download within a user interaction event
    link.dispatchEvent(new MouseEvent('click'));

  } catch (error) {
    console.error(error);
  }
}

async function copyItem() {
  if (fileManager.value.selected.length === 0) {
    return
  };
  try {
    const response = await storeAuth.axiosInstance.post(`${server}/manager/${fileManager.value.action}`, {
      'item': fileManager.value.selected,
      'old': fileManager.value.copied
      });
    console.log(response.data);
    getFoldersFiles();
  
  } catch (error) {
    console.error(error);
  }
};

async function updateItem() {
  try {
    const response = fileManager.value.action === 'create'
      ? await storeAuth.axiosInstance.post(`${server}/manager/${fileManager.value.action}`, {
        'item': modalValue.value
        })
      : await storeAuth.axiosInstance.patch(`${server}/manager/${fileManager.value.action}`, {
        'old': fileManager.value.selected[0],
        'new': modalValue.value
      });
    console.log(response.data);
    getFoldersFiles();
  
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
        'items': fileManager.value.selected
        });
      console.log(response.data);
      getFoldersFiles();
   
    } catch (error) {
      console.error(error);
    }
  }
};

</script>

<template>
  <div class="container py-3">
    
    <HeaderDiv page-header="Файловый менеджер" />

    <div class="border border-primary p-5" id="fileManager">

      <div class="row border border-primary p-3">
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="fileManager.action = 'create'"
            data-bs-toggle="modal" data-bs-target="#modalItem"
            :disabled="fileManager.select">
            <i class="bi bi-plus-square" title="Создать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="fileManager.select = !fileManager.select">
            <i class="bi bi-check-square" title="Выбрать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
            @click="fileManager.action = 'copy'; fileManager.copied = fileManager.selected"
            :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-clipboard" title="Копировать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
            @click="fileManager.action = 'сut'; fileManager.copied = fileManager.selected"
            :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-scissors" title="Вырезать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="!fileManager.select || fileManager.selected.length === 0"
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
            @click="deleteItem" :disabled="!fileManager.select || fileManager.selected.length === 0">
            <i class="bi bi-trash" title="Удалить"></i>
          </button>
        </div>
      </div>
    
      <div class="py-3">
        <nav aria-label="breadcrumb">
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
        <li class="list-group-item">
          <a href="#" class="list-group-item list-group-item-action" title="Наверх"
            @click="openFolder(fileManager.path[-1])">
            <i class="bi bi-arrow-90deg-up"></i>
          </a>
        </li>

        <li class="list-group-item" v-for="folder in fileManager.folders" :key="folder">
          <div class="item-wrapper fs-6">
            <input class="form-check-input" type="checkbox" v-if="fileManager.select" 
                  :value="folder" v-model="fileManager.selected">
            &nbsp;
            <a href="#" class="list-group-item-action" @click="openFolder(folder)">
              <i class="bi bi-folder"></i>
              {{ folder }}
            </a>
          </div>
        </li>

        <li class="list-group-item" v-for="file in fileManager.files" :key="file">
          <div class="item-wrapper">
            <input class="form-check-input" type="checkbox" v-if="fileManager.select"
                  :value="file" v-model="fileManager.selected">
            &nbsp; &nbsp;
            <a href="#" class="list-group-item list-group-item-action"
              @click="openFile(file)">
              <i class="bi bi-file"></i>
              {{ file }}
            </a>
          </div>
        </li>
      </ul>
    </div>
    
    <div class="modal fade" id="modalItem" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
      <div class="modal-dialog modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="modalWinLabel">{{ modalHeader }}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            
            <form @submit.prevent="updateItem" class="form form-check" role="form">
              <div class="mb-3 row">
                <div class="col-10">
                  <input class="form-control" id="name" maxlength="250" name="name" type="text"
                  v-model="modalValue">
                </div>
                <div class="col-2">
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
  height: 100vh;
  max-height: 100vh;
  overflow-y: auto;
}
.list-group-item .item-wrapper {
  display: flex;
  align-items: center;
}
</style>