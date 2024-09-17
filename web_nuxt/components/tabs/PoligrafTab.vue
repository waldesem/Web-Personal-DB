<script setup lang="ts">
import { server } from "@/state/state";
import type { Pfo } from "@/types/interfaces";

const toast = useToast();

const editState = inject("editState") as boolean;
const candId = inject("candId") as string;

const edit = ref(false);
cons collapse = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);

const { data: poligrafs, refresh } = await useLazyAsyncData("poligrafs", async () => {
  const response = await authFetch(
    `${server}/poligrafs/${candId}`
    );
  return response
});

async function updatePoligraf(form: Pfo) {
  closeAction();
  const response = await authFetch(
    `${server}/poligrafs/${candId}`,
      {
        method: "POST",
        body: form,
      }
    );
    console.log(response);
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Успешно",
      description: "Информация обновлена",
      color: "green",
    });
  }
  refresh();
}

async function deletePoligraf(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch(`${server}/poligrafs/${id}`, {
    method: "DELETE",
  });
  console.log(response);
  toast.add({
      icon: "i-heroicons-information-circle",
      title: "Информация",
      description: `Запись с ID ${id} удалена`,
      color: "primary",
    });
  }
  refresh();
}

async function submitFile(fileList: FileList): Promise<void> {
  const formData = new FormData();
  if (fileList) {
    for (const file of fileList) {
      formData.append("file", file);
      }
    const response = await authFetch(`${server}/file/$poligrafs/${candId}`, {
        method: "POST",
        body: formData,
      });
      console.log(response);
      toast.add({
        icon: "i-heroicons-check-circle",
        title: response["message"] == "success" ? "Информация" : "Внимание",
        description: `Файлы успешно загружены`,
        color: "green",
      });
    }
  formData.delete("file");
}

async function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  collapse = false;
  edit.value = false;
  itemId.value = "";
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}
</script>

<template>
  <UButton
    v-if="editState"
    class="py-3"
    :label="collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsPoligrafForm @cancel="cancelOperation" @submit="updatePoligraf" />
      </UCard>
    </div>
  </Transition>
  <div
    v-if="
      poligrafs &&
      poligrafs.length
    "
  >
    <div
      v-for="(item, index) in poligrafs"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <UCard>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Обследование на полиграфе ID #" + item["id"] }}
          </div>
        </template>
        <FormsPoligrafForm
          v-if="edit && itemId == item['id'].toString()"
          :poligraf="poligraf"
          @cancel="cancelOperation"
          @submit="updatePoligraf"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тема проверки'">{{
            item["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Результат'">{{
            item["results"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            @update="
              poligraf = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deletePoligraf(item['id'])"
            @upload="openFileForm('poligraf-file')"
          />
          <div v-show="false">
            <UInput
              id="poligraf-file"
              type="file"
              accept="*"
              multiple
              @change="
                anketaState.submitFile(
                  $event,
                  'poligrafs',
                  anketaState.share.value.candId
                )
              "
            />
          </div>
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-red-800">Обследование на полиграфе не проводилось</p>
  </div>
</template>
