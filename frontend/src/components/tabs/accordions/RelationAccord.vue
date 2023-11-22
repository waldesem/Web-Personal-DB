<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionRelation" v-if="props.store.relate.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.relate" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseRelation${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseRelation${tbl['id']}`" class="accordion-collapse collapse" 
          :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionRelation">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('relation', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('relation', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Тип связи</td><td>{{ tbl['relation'] }}</td></tr>
            <tr v-if="tbl['relation_id']">
              <td>Связь</td>
              <td>
                <router-link
                  :to="{ name: 'profile', params: { group: 'staffsec', id: String(tbl['relation_id']) } }">
                  ID #{{ tbl['relation_id'] }}
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>