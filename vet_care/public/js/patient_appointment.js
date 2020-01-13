var check_and_set_availability = function(frm) {
  var selected_slot = null;
  var service_unit = null;
  var duration = null;

  show_availability();

  function show_empty_state(practitioner, appointment_date) {
    frappe.msgprint({
      title: __("Not Available"),
      message: __("Healthcare Practitioner {0} not available on {1}", [
        practitioner.bold(),
        appointment_date.bold()
      ]),
      indicator: "red"
    });
  }

  function show_availability() {
    let selected_practitioner = "";
    var d = new frappe.ui.Dialog({
      title: __("Available slots"),
      fields: [
        {
          fieldtype: "Link",
          options: "Medical Department",
          fieldname: "department",
          label: "Medical Department"
        },
        { fieldtype: "Column Break" },
        {
          fieldtype: "Link",
          options: "Healthcare Practitioner",
          reqd: 1,
          fieldname: "practitioner",
          label: "Healthcare Practitioner"
        },
        { fieldtype: "Column Break" },
        {
          fieldtype: "Date",
          reqd: 1,
          fieldname: "appointment_date",
          label: "Date"
        },
        { fieldtype: "Section Break" },
        { fieldtype: "HTML", fieldname: "available_slots" }
      ],
      primary_action_label: __("Book"),
      primary_action: function() {
        frm.set_value("appointment_time", selected_slot);
        frm.set_value("service_unit", service_unit || "");
        frm.set_value("duration", duration);
        frm.set_value("practitioner", d.get_value("practitioner"));
        frm.set_value("department", d.get_value("department"));
        frm.set_value("appointment_date", d.get_value("appointment_date"));
        d.hide();
        frm.enable_save();
        frm.save();
        frm.enable_save();
        d.get_primary_btn().attr("disabled", true);
      }
    });

    d.set_values({
      department: frm.doc.department,
      practitioner: frm.doc.practitioner,
      appointment_date: frm.doc.appointment_date
    });

    d.fields_dict["department"].df.onchange = () => {
      d.set_values({
        practitioner: ""
      });
      var department = d.get_value("department");
      if (department) {
        d.fields_dict.practitioner.get_query = function() {
          return {
            filters: {
              department: department
            }
          };
        };
      }
    };

    // disable dialog action initially
    d.get_primary_btn().attr("disabled", true);

    // Field Change Handler

    var fd = d.fields_dict;

    d.fields_dict["appointment_date"].df.onchange = () => {
      show_slots(d, fd);
    };
    d.fields_dict["practitioner"].df.onchange = () => {
      if (
        d.get_value("practitioner") &&
        d.get_value("practitioner") != selected_practitioner
      ) {
        selected_practitioner = d.get_value("practitioner");
        show_slots(d, fd);
      }
    };
    d.show();
  }

  function show_slots(d, fd) {
    if (d.get_value("appointment_date") && d.get_value("practitioner")) {
      fd.available_slots.html("");
      frappe.call({
        method:
          "erpnext.healthcare.doctype.patient_appointment.patient_appointment.get_availability_data",
        args: {
          practitioner: d.get_value("practitioner"),
          date: d.get_value("appointment_date")
        },
        callback: r => {
          var data = r.message;
          if (data.slot_details.length > 0) {
            var $wrapper = d.fields_dict.available_slots.$wrapper;

            // make buttons for each slot
            var slot_details = data.slot_details;
            var slot_html = "";
            for (let i = 0; i < slot_details.length; i++) {
              slot_html =
                slot_html + `<label>${slot_details[i].slot_name}</label>`;
              slot_html =
                slot_html +
                `<br/>` +
                slot_details[i].avail_slot
                  .map(slot => {
                    let disabled = "";
                    let start_str = slot.from_time;
                    let slot_start_time = moment(slot.from_time, "HH:mm:ss");
                    let slot_to_time = moment(slot.to_time, "HH:mm:ss");
                    let interval =
                      ((slot_to_time - slot_start_time) / 60000) | 0;
                    // iterate in all booked appointments, update the start time and duration
                    slot_details[i].appointments.forEach(function(booked) {
                      let booked_moment = moment(
                        booked.appointment_time,
                        "HH:mm:ss"
                      );
                      let end_time = booked_moment
                        .clone()
                        .add(booked.duration, "minutes");
                      // Deal with 0 duration appointments
                      if (
                        booked_moment.isSame(slot_start_time) ||
                        booked_moment.isBetween(slot_start_time, slot_to_time)
                      ) {
                        if (booked.duration == 0) {
                          disabled = 'disabled="disabled"';
                          return false;
                        }
                      }
                      // Check for overlaps considering appointment duration
                      if (
                        slot_start_time.isBefore(end_time) &&
                        slot_to_time.isAfter(booked_moment)
                      ) {
                        // There is an overlap
                        disabled = 'disabled="disabled"';
                        return false;
                      }
                    });
                    return `<button class="btn btn-default"
									data-name=${start_str}
									data-duration=${interval}
									data-service-unit="${slot_details[i].service_unit || ""}"
									style="margin: 0 10px 10px 0; width: 72px;" ${disabled}>
									${start_str.substring(0, start_str.length - 3)}
								</button>`;
                  })
                  .join("");
              slot_html = slot_html + `<br/>`;
            }

            $wrapper
              .css("margin-bottom", 0)
              .addClass("text-center")
              .html(slot_html);

            // blue button when clicked
            $wrapper.on("click", "button", function() {
              var $btn = $(this);
              $wrapper.find("button").removeClass("btn-primary");
              $btn.addClass("btn-primary");
              selected_slot = $btn.attr("data-name");
              service_unit = $btn.attr("data-service-unit");
              duration = $btn.attr("data-duration");
              // enable dialog action
              d.get_primary_btn().attr("disabled", null);
            });
          } else {
            //	fd.available_slots.html("Please select a valid date.".bold())
            show_empty_state(
              d.get_value("practitioner"),
              d.get_value("appointment_date")
            );
          }
        },
        freeze: true,
        freeze_message: __("Fetching records......")
      });
    } else {
      fd.available_slots.html(
        "Appointment date and Healthcare Practitioner are Mandatory".bold()
      );
    }
  }
};
