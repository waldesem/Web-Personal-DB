<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const ContactForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/ContactForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "contact");
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

const contact = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<any, string>>{},
});

function deactivateEmit() {
  contact.value.isForm = false; 
  contact.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [contact.value.action, "contact", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "contact"])
};
</script>

<template>
  <h6>
    Контакты
    <a
      class="btn btn-link"
      @click="
        contact.isForm = !contact.isForm;
        contact.action = contact.isForm ? 'create' : '';"
      :title="contact.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="contact.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="contact.isForm">
    <ContactForm 
      :action="contact.action"
      :cand-id="candId"
      :content="contact.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'cont' + idx.toString()"
        :idx="idx.toString()"
        :label="'Контакт #' + (idx + 1).toString()"
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
                contact.isForm = true;
                contact.action = 'update';
                contact.item = item;
                contact.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Вид'" :value="item['view']" />
        <RowDivSlot :label="'Контакт'" :value="item['contact']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
