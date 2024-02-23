  interface Pfo {
    id: string;
    theme: string;
    results: string;
    officer: string;
    deadline: string;
  };
  
  interface Inquisition {
    id: string;
    theme: string;
    info: string;
    officer: string;
    deadline: string;
  };
  
  interface Needs {
    id: string;
    info: string;
    initiator: string;
    source: string;
    officer: string;
    deadline: string;
  };
  

  const dataChecks = ref({

    getItem: async function (): Promise<void> {
      if (
        dataProfile.value.item === "check" &&
        dataProfile.value.action === "add"
      ) {
        if (
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "save" ||
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "manual" ||
          classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
            "robot"
        ) {
          storeAlert.alertMessage.setAlert(
            "alert-warning",
            "Нельзя добавить проверку к текущему статусу"
          );
          return;
        }
      }
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/${dataProfile.value.item}/${dataProfile.value.candId}`,
          {
            params: {
              action: dataProfile.value.action,
            },
          }
        );
        switch (dataProfile.value.item) {
          case "check":
            this.verification = response.data;
            break;
          case "robot":
            this.robot = response.data;
            break;
          case "poligraf":
            this.pfo = response.data;
            break;
          case "investigation":
            this.inquisition = response.data;
            break;
          case "inquiry":
            this.needs = response.data;
            break;
          default:
            console.log(response.data);
            break;
        }
        if (
          dataProfile.value.item === "check" &&
          (dataProfile.value.action === "add" ||
            dataProfile.value.action === "self")
        ) {
          this.getItem();
        }
      } catch (error) {
        console.error(error);
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Ошибка обработки ${error}`
        );
      }
    },

    deleteItem: async function (): Promise<void> {
      if (
        classifyApp.classData.status[dataResume.value.resume["status_id"]] ===
        "robot"
      ) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Нельзя удалить запись из анкеты текущим статусом"
        );
        return;
      }
      if (confirm(`Вы действительно хотите удалить запись?`)) {
        try {
          const response = await storeAuth.axiosInstance.delete(
            `${server}/${dataProfile.value.item}${dataProfile.value.itemId}`
          );
          console.log(response.status);
          this.getItem();

          storeAlert.alertMessage.setAlert(
            "alert-info",
            `Запись с ID ${dataProfile.value.itemId} удалена`
          );
        } catch (error) {
          console.error(error);
        }
      }
    },
  });

  return { dataProfile, dataResume, dataAnketa, dataChecks };
});
