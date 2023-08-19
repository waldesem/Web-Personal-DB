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
  emit('formItem', { 'view': formData.value['view'], 'contact': formData.value['contact']});
}

</script>

<template>
   <form @submit.prevent="submitData" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
        <select class="form-select" id="view" name="view" v-model="formData['view']">
            <option value="Телефон">Телефон</option>
            <option value="E-mail">E-mail</option>
            <option value="Другое">Другое</option>
        </select>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="contact">Контакт</label>
        <div class="col-lg-10">
        <input class="form-control" id="contact" maxlength="250" name="contact" required type="text" v-model="formData['contact']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
