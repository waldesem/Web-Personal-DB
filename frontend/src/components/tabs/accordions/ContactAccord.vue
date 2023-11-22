<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionContact" v-if="props.store.conts.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.conts" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseContact${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseContact${tbl['id']}`" class="accordion-collapse collapse" 
          :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionContact">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('contact', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('contact', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Вид</td>
              <td>{{ tbl['view'] ? tbl['view'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Контакт</td>
              <td>{{ tbl['contact'] ? tbl['contact'] : 'Данные отсутствуют' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>