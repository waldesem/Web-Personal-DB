<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const ContactForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/ContactForm.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get-item", "contact");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const contact = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit(){
  contact.value.action = '';
  contact.value.item = {};
};

function submitForm(form: Object) {
  emit("submit", [contact.value.action, "contact", contact.value.itemId, form])
   cancelEdit();
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "contact"])
};
</script>

<template>
  <h6>
    Контакты
    <a
      data-bs-toggle="modal"
      data-bs-target="#modalContact"
      class="btn btn-link"
      @click="contact.action = 'create'"
      title="Добавить информацию"
    >
      <i class="bi bi-plus-circle"></i>
    </a>
  </h6>
  <ModalWin
    :title="
      contact.action === 'update' ? 'Изменить адрес' : 'Добавить адрес'
    "
    :id="'modalContact'"
    @cancel="cancelEdit"
  >
    <ContactForm 
      :content="contact.item"
      @submit="submitForm"
    />
  </ModalWin>
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
            data-bs-toggle="modal"
            data-bs-target="#modalContact"
            class="btn btn-link"
            title="Изменить"
            @click="
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
