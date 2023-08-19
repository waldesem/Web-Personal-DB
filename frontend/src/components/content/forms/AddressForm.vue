<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 

import { toRef } from 'vue';

const emit = defineEmits(['formItem']);

const props = defineProps({
    item: {
        type: Object,
        required: true,
        default: () => ({})
    }
});

const formData = toRef(props.item);


 /**
  * Updates or adds an item.
  *
  * @return {void} 
  */
 function submitData(): void {
  emit('formItem', {
    'view': formData.value['view'], 
    'region': formData.value['region'], 
    'address': formData.value['address']
});
}

</script>

<template>
   <form @submit.prevent="submitData" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
        <select class="form-select" id="view" name="view" v-model="formData['view']">
            <option value="Адрес регистрации">Адрес регистрации</option>
            <option value="Адрес проживания">Адрес проживания</option>
            <option value="Другое">Другое</option>
        </select>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
        <input class="form-control" id="region" maxlength="250" name="region" type="text" v-model="formData['region']">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="address">Полный адрес</label>
        <div class="col-lg-10">
        <input class="form-control" id="address" maxlength="250" name="address" required type="text" v-model="formData['address']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
  </form>
</template>
