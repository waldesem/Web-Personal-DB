<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/RelationForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "relation");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const relation = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<any, string>>{},
});

function deactivateEmit() {
  relation.value.isForm = false; 
  relation.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [relation.value.action, "relation", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "relation"])
};
</script>

<template>
  <h6>
    Связи
    <a
      class="btn btn-link"
      @click="
        relation.isForm = !relation.isForm;
        relation.action = relation.isForm ? 'create' : '';"
      :title="relation.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="relation.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="relation.isForm">
    <RelationForm
      :action="relation.action"
      :cand-id="candId"
      :content="relation.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'relate' + idx.toString()"
        :idx="idx.toString()"
        :label="'Связь #' + (idx + 1).toString()"
      >
      <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                relation.isForm = true;
                relation.action = 'update';
                relation.item = item;
                relation.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Тип связи'" :value="item['relation']" />
        <RowDivSlot :label="'Связь'" :slotTwo="true">
          <router-link
            :to="{
              name: 'profile',
              params: { id: String(item['relation_id']) },
            }"
          >
            ID #{{ item["relation_id"] }}
          </router-link>
        </RowDivSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
