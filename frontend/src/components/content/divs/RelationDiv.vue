<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Relation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/CollapseDiv.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/RelationForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async () => {
  emit("get-item", "relation");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Relation>,
    default: {},
  },
});

const relation = ref({
  action: "",
  itemId: "",
  item: <Relation>{},
});

function submitForm(form: Object) {
  emit("submit", 
    relation.value.action,
    "relation",
    relation.value.itemId,
    form,
  );
  relation.value.action = "";
};
</script>

<template>
  <h6>
    Связи
    <a
      class="btn btn-link"
      @click="relation.action = relation.action ? '' : 'create'"
      :title="relation.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="relation.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <RelationForm v-if="relation.action"
    :content="relation.item"
    @submit="submitForm"
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'relate' + idx"
        :idx="idx.toString()"
        :label="'Связь #' + (idx + 1)"
      >
        <LabelValue :label="'Действия'" :no-print="true">
          <a
            href="#" 
            @click="emit('delete', item['id'].toString(), 'relation')" 
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              relation.action = 'update';
              relation.item = item;
              relation.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelValue>
        <LabelValue :label="'ID'">{{ item["id"] }}</LabelValue>
        <LabelValue :label="'Тип'">{{ item["relation"] }}</LabelValue>
        <LabelValue :label="'Связь'" :no-print="true">
          <router-link
            :to="{
              name: 'profile',
              params: { id: String(item['relation_id']) },
            }"
          >
            ID #{{ item["relation_id"] }}
          </router-link>
        </LabelValue>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
