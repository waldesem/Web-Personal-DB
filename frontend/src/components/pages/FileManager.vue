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
  files: []
});

const selectedItems = ref([]);
const itemName = ref("");
const action = ref("");
const modalHeader = ref("Создать папку");

async function getFoldersFiles() {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/files`);
    const { path, dirs, files }= response.data;
    fileManager.value.path = path;
    fileManager.value.folders = dirs;
    fileManager.value.files = files;

  } catch (error) {
    console.error(error);
  }
};

async function updateItem() {
  try {
    const response = action.value === 'create'
      ? await storeAuth.axiosInstance.post(`${server}/files/${action.value}`, {
        'item': itemName.value
        })
      : await storeAuth.axiosInstance.patch(`${server}/files/${action.value}`, {
        'old': selectedItems.value[0],
        'new': itemName.value
      });
    console.log(response.data);
    getFoldersFiles();
  
  } catch (error) {
    console.error(error);
  }
};

async function deleteItem() {
  if (selectedItems.value.length === 0) {
    return
  };
  if (confirm("Вы действительно хотите удалить?")) {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/files/delete`, {
        'items': selectedItems.value
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
    
    <di>
      <button type="button" class="btn btn-outline-dark" title="Создать"
        @click="action = 'create'; modalHeader = 'Создать папку'"
        data-bs-toggle="modal" data-bs-target="#modalItem">
        <i class="bi bi-plus-square"></i>
      </button>
      
      <button type="button" class="btn btn-outline-info" title="Выбрать">
        <i class="bi bi-check-square"></i>
      </button>
      
      <button type="button" class="btn btn-outline-primary" title="Копировать">
        <i class="bi bi-clipboard"></i>
      </button>
      
      <button type="button" class="btn btn-outline-secondary" title="Вырезать">
        <i class="bi bi-scissors"></i>
      </button>
      
      <button type="button" class="btn btn-outline-success" title="Вставить">
        <i class="bi bi-file-clipboard-fill"></i>
      </button>
      
      <button type="button" class="btn btn-outline-warning" title="Переменовать"
        @click="action = 'rename'; modalHeader = 'Переименовать папку'"
        data-bs-toggle="modal" data-bs-target="#modalItem">
        <i class="bi bi-repeat"></i>
      </button>
      
      <button type="button" class="btn btn-outline-danger" title="Удалить"
        @click="deleteItem">
        <i class="bi bi-trash"></i>
      </button>
    </di>

    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item active" aria-current="page" 
            v-for="item in fileManager.path" :key="item">
          {{ item }}
        </li>
      </ol>
    </nav>

    <ul class="list-group">
      <a href="#" class="list-group-item list-group-item-action" 
                  v-for="folder in fileManager.folders" :key="folder">
        <i class="bi bi-folder"></i>
        {{ folder  }}
      </a>
      <a href="#" class="list-group-item list-group-item-action" 
                  v-for="file in fileManager.files" :key="file">
        <i class="bi bi-file"></i>
        {{ file }}
      </a>    
    </ul>
  
    <div class="modal fade" id="modalItem" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
      <div class="modal-dialog modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="modalWinLabel">Создать папку</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            
            <form @submit.prevent="updateItem" class="form form-check" role="form">
              <div class="mb-3 row">
                <div class="col-10">
                  <input class="form-control" id="name" maxlength="250" name="name" type="text"
                  v-model="itemName">
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