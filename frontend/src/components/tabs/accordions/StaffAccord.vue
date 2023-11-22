<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionStaff" v-if="props.store.staffs.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.staffs" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseStaff${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseStaff${tbl['id']}`" class="accordion-collapse collapse" 
          :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionStaff">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('staff', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('staff', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Должность</td>
              <td>{{ tbl['position'] ? tbl['position'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Департамент</td>
              <td>{{ tbl['department'] ? tbl['department'] : 'Данные отсутствуют' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>