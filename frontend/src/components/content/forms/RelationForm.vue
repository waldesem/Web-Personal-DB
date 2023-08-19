<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 

import { toRef } from 'vue';

const emit = defineEmits(['formItem', 'cancelEdit']);

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
    'relation': formData.value['relation'], 
    'relation_id': formData.value['relation_id']
});
}

</script>

<template>
   <form @submit.prevent="submitData" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="relation">Тип связи</label>
        <div class="col-lg-10">
        <input class="form-control" id="relation" maxlength="250" name="relation" type="text" v-model="formData['relation']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="relation_id">ID связи</label>
        <div class="col-lg-10">
        <input class="form-control" id="relation_id" maxlength="25" name="relation_id" type="text" v-model="formData['relation_id']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
