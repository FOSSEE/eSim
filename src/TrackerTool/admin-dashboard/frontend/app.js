function $(id){ return document.getElementById(id); }

function loadConfig() {
  if (!localStorage.getItem("ADMIN_API_URL")) {
    localStorage.setItem("ADMIN_API_URL", "http://127.0.0.1:5001");
  }

  if (!localStorage.getItem("ADMIN_TOKEN")) {
    localStorage.setItem("ADMIN_TOKEN", "12345");
  }
}


function saveConfig() {
  const apiUrlEl = document.getElementById("apiUrl");
  const adminTokenEl = document.getElementById("adminToken");

  if (apiUrlEl) {
    localStorage.setItem("apiUrl", apiUrlEl.value.trim());
  }

  if (adminTokenEl) {
    localStorage.setItem("adminToken", adminTokenEl.value.trim());
  }
}

function apiBase(){
  return (localStorage.getItem("ADMIN_API_URL") || "http://127.0.0.1:5001").replace(/\/+$/,"");
}

function adminToken(){
  return localStorage.getItem("ADMIN_TOKEN") || "";
}

async function apiGet(path){
  const res = await fetch(`${apiBase()}${path}`, {
    headers: { "X-Admin-Token": adminToken() }
  });
  if(!res.ok){
    const t = await res.text();
    throw new Error(`${res.status} ${t}`);
  }
  return res.json();
}

async function apiPost(path, data){
  const res = await fetch(`${apiBase()}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Token": adminToken()
    },
    body: JSON.stringify(data || {})
  });
  if(!res.ok){
    const t = await res.text();
    throw new Error(`${res.status} ${t}`);
  }
  return res.json();
}

async function apiPut(path, data){
  const res = await fetch(`${apiBase()}${path}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Token": adminToken()
    },
    body: JSON.stringify(data || {})
  });
  if(!res.ok){
    const t = await res.text();
    throw new Error(`${res.status} ${t}`);
  }
  return res.json();
}

async function apiDelete(path){
  const res = await fetch(`${apiBase()}${path}`, {
    method: "DELETE",
    headers: { "X-Admin-Token": adminToken() }
  });
  if(!res.ok){
    const t = await res.text();
    throw new Error(`${res.status} ${t}`);
  }
  return res.json();
}

function setPage(title, sub){
  $("pageTitle").textContent = title;
  $("pageSub").textContent = sub;
}

function setView(view){
  document.querySelectorAll(".view").forEach(v=>v.classList.remove("active"));
  const target = document.querySelector(`#view-${view}`);
  if(target) target.classList.add("active");

  document.querySelectorAll(".nav-btn").forEach(b=>b.classList.remove("active"));
  const navBtn = document.querySelector(`.nav-btn[data-view="${view}"]`);
  if(navBtn) navBtn.classList.add("active");

  if(view==="overview"){ setPage("Overview","System summary & latest activity."); }
  if(view==="sessions"){ setPage("Sessions","Browse tracked sessions across users."); }
  if(view==="logs"){ setPage("Logs","Review stored logs across users."); }
  if(view==="crashes"){ setPage("Crashes","Search, filter, group & export crash events."); }
  if(view==="tasks"){ setPage("Tasks","Track development work, bugs, features, testing, and documentation."); }
  if(view==="releases"){ setPage("Releases","Manage milestones, versions, and linked task progress."); }
  if(view==="visuals"){ setPage("Visualizations","Charts & trends for sessions and crashes."); }
  if(view==="locations"){ setPage("Locations","View captured session locations (IP-based)."); }
}

function escapeHtml(s){
  return String(s ?? "")
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function downloadCSV(filename, rows){
  const csv = rows.map(r => r.map(v => `"${String(v ?? "").replaceAll('"','""')}"`).join(",")).join("\n");
  const blob = new Blob([csv], {type:"text/csv;charset=utf-8;"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function tableHtml(headers, rows){
  const th = headers.map(h=>`<th>${escapeHtml(h)}</th>`).join("");
  const tr = rows.map(r=>`<tr>${r.map(c=>`<td>${escapeHtml(c)}</td>`).join("")}</tr>`).join("");
  return `<div class="table-scroll"><table class="table"><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table></div>`;
}

function buildQuery(paramsObj = {}){
  const sp = new URLSearchParams();
  Object.entries(paramsObj).forEach(([k, v]) => {
    if(v !== undefined && v !== null && String(v).trim() !== ""){
      sp.set(k, String(v).trim());
    }
  });
  const q = sp.toString();
  return q ? `?${q}` : "";
}

async function loadUsers(){
  const users = await apiGet("/admin/users");
  const sel = $("userFilter");
  sel.innerHTML = `<option value="">All Users</option>`;
  users.forEach(u=>{
    const opt = document.createElement("option");
    opt.value = u;
    opt.textContent = u;
    sel.appendChild(opt);
  });
}

/* -------------------------
   OVERVIEW / SESSIONS / LOGS / CRASHES
-------------------------- */
async function renderOverview(){
  const data = await apiGet("/admin/overview");

  const wrap = $("view-overview");
  wrap.innerHTML = `
    <div class="kpi-grid">
      <div class="card kpi">
        <div class="kpi-title">Total Users</div>
        <div class="kpi-value">${data.users_count}</div>
      </div>
      <div class="card kpi">
        <div class="kpi-title">Sessions (Last 7 days)</div>
        <div class="kpi-value">${data.sessions_7d}</div>
      </div>
      <div class="card kpi">
        <div class="kpi-title">Crashes (Last 7 days)</div>
        <div class="kpi-value">${data.crashes_7d}</div>
      </div>
    </div>

    <div class="table-wrap">
      <div class="table-title">Latest Sessions</div>
      ${tableHtml(
        ["User","Start","End","Duration"],
        (data.latest_sessions || []).map(s => [s.user_id, s.session_start, s.session_end, s.total_duration])
      )}
    </div>

    <div class="table-wrap">
      <div class="table-title">Latest Crashes</div>
      ${tableHtml(
        ["Crash ID","User","Time","Exception","Module","Event"],
        (data.latest_crashes || []).map(c => [c.crash_id, c.user_id, c.crash_time, c.exception_code, c.faulting_module, c.event_id])
      )}
    </div>
  `;
}

async function renderSessions(){
  const user = $("userFilter").value.trim();
  const q = buildQuery({ user });
  const rows = await apiGet(`/admin/sessions${q}`);

  const wrap = $("view-sessions");
  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Sessions Table</div>
      <div class="muted" style="margin-top:6px;">Tip: filter by user using the top-right dropdown.</div>

      <div class="table-wrap">
        ${tableHtml(
          ["Session ID","User","Start","End","Duration"],
          rows.map(s => [s.session_id, s.user_id, s.session_start, s.session_end, s.total_duration])
        )}
      </div>

      <div style="margin-top:12px;">
        <button class="btn" id="exportSessions">Export CSV</button>
      </div>
    </div>
  `;

  $("exportSessions").onclick = () => {
    const csvRows = [
      ["session_id","user_id","session_start","session_end","total_duration"],
      ...rows.map(s => [s.session_id, s.user_id, s.session_start, s.session_end, s.total_duration])
    ];
    downloadCSV("admin_sessions.csv", csvRows);
  };
}

function parseLocation(loc){
  if(!loc) return null;
  if(typeof loc === "object") return loc;
  if(typeof loc === "string"){
    try { return JSON.parse(loc); } catch { return { raw: loc }; }
  }
  return null;
}

function mapLink(lat, lon){
  if(lat == null || lon == null || lat === "" || lon === "") return "";
  const url = `https://www.google.com/maps?q=${encodeURIComponent(lat)},${encodeURIComponent(lon)}`;
  return `<a class="link" href="${url}" target="_blank" rel="noopener">Open</a>`;
}

async function renderLocations(){
  const user = $("userFilter").value.trim();
  const q = buildQuery({ user });

  const rows = await apiGet(`/admin/sessions${q}`);

  const withLoc = rows
    .map(s => {
      const loc = parseLocation(s.location);
      return { ...s, _loc: loc };
    })
    .filter(s => s._loc);

  const wrap = $("view-locations");

  if(!withLoc.length){
    wrap.innerHTML = `
      <div class="card">
        <div class="section-title">Locations</div>
        <div class="muted" style="margin-top:6px;">No location data found for this filter.</div>
      </div>
    `;
    return;
  }

  withLoc.sort((a,b)=> (b.session_id||0) - (a.session_id||0));

  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Locations</div>
      <div class="muted" style="margin-top:6px;">
        Showing ${withLoc.length} sessions with locations.
      </div>

      <div class="table-wrap" style="margin-top:12px;">
        <div class="table-scroll">
          <table class="table">
            <thead>
              <tr>
                <th>Session ID</th>
                <th>User</th>
                <th>Start</th>
                <th>End</th>
                <th>IP</th>
                <th>City</th>
                <th>Region</th>
                <th>Country</th>
                <th>Lat</th>
                <th>Lon</th>
                <th>Map</th>
              </tr>
            </thead>
            <tbody>
              ${withLoc.map(s=>{
                const loc = s._loc || {};
                const lat = loc.latitude ?? loc.lat ?? "";
                const lon = loc.longitude ?? loc.lon ?? "";
                return `
                  <tr>
                    <td>${escapeHtml(s.session_id)}</td>
                    <td>${escapeHtml(s.user_id)}</td>
                    <td>${escapeHtml(s.session_start)}</td>
                    <td>${escapeHtml(s.session_end)}</td>
                    <td>${escapeHtml(loc.ip || "")}</td>
                    <td>${escapeHtml(loc.city || "")}</td>
                    <td>${escapeHtml(loc.region || loc.regionName || "")}</td>
                    <td>${escapeHtml(loc.country || "")}</td>
                    <td>${escapeHtml(lat)}</td>
                    <td>${escapeHtml(lon)}</td>
                    <td>${mapLink(lat, lon)}</td>
                  </tr>
                `;
              }).join("")}
            </tbody>
          </table>
        </div>
      </div>

      <div style="margin-top:12px;">
        <button class="btn" id="exportLocations">Export CSV</button>
      </div>
    </div>
  `;

  $("exportLocations").onclick = () => {
    const csvRows = [
      ["session_id","user_id","session_start","session_end","ip","city","region","country","latitude","longitude"],
      ...withLoc.map(s=>{
        const loc = s._loc || {};
        return [
          s.session_id,
          s.user_id,
          s.session_start,
          s.session_end,
          loc.ip || "",
          loc.city || "",
          loc.region || loc.regionName || "",
          loc.country || "",
          loc.latitude ?? loc.lat ?? "",
          loc.longitude ?? loc.lon ?? ""
        ];
      })
    ];
    downloadCSV("admin_locations.csv", csvRows);
  };
}

async function renderLogs(){
  const user = $("userFilter").value.trim();
  const q = buildQuery({ user });
  const rows = await apiGet(`/admin/logs${q}`);

  const wrap = $("view-logs");
  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Logs</div>
      <div class="muted" style="margin-top:6px;">Click a row to view full log details.</div>

      <div class="table-wrap">
        ${tableHtml(
          ["Log ID","User","Timestamp","Preview"],
          rows.map(l => [l.log_id, l.user_id, l.log_timestamp, String(l.log_content||"").slice(0,80)])
        )}
      </div>

      <div style="margin-top:12px;">
        <button class="btn" id="exportLogs">Export CSV</button>
      </div>

      <div class="card" style="margin-top:12px;">
        <div class="section-title">Selected Log</div>
        <pre id="logDetails" class="muted" style="margin-top:10px;">Select a log from the table above.</pre>
      </div>
    </div>
  `;

  const table = wrap.querySelector("table");
  table.querySelectorAll("tbody tr").forEach((tr, idx)=>{
    tr.style.cursor = "pointer";
    tr.onclick = () => {
      $("logDetails").textContent =
        `User: ${rows[idx].user_id}\nTimestamp: ${rows[idx].log_timestamp}\n\n${rows[idx].log_content || ""}`;
    };
  });

  $("exportLogs").onclick = () => {
    const csvRows = [
      ["log_id","user_id","log_timestamp","log_content"],
      ...rows.map(l => [l.log_id, l.user_id, l.log_timestamp, l.log_content])
    ];
    downloadCSV("admin_logs.csv", csvRows);
  };
}

async function renderCrashes(){
  const user = $("userFilter").value.trim();

  const wrap = $("view-crashes");
  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Crash Monitoring & Analysis</div>
      <div class="muted" style="margin-top:6px;">
        Search + filter crashes, view details, and analyze grouped signatures.
      </div>

      <div class="filter-card card" style="margin-top:12px;">
        <div class="filters">
          <div class="field">
            <label>Search</label>
            <input id="crashQ" class="control" type="text" placeholder="Search message/module/exception..." />
          </div>
          <div class="field">
            <label>Exception code</label>
            <input id="crashExc" class="control" type="text" placeholder="0xc0000409" />
          </div>
          <div class="field">
            <label>Faulting module</label>
            <input id="crashMod" class="control" type="text" placeholder="ucrtbase.dll" />
          </div>
          <div class="field field-actions">
            <label>&nbsp;</label>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button class="btn primary" id="crashApply">Apply</button>
              <button class="btn" id="crashClear">Clear</button>
            </div>
          </div>
        </div>
      </div>

      <div class="split" style="margin-top:12px;">
        <div class="card">
          <div class="section-title">Crash List</div>
          <div class="muted" style="margin-top:6px;">Select a crash to view full details.</div>
          <div style="height:10px"></div>
          <div id="crashList" class="list"></div>

          <div style="margin-top:12px;">
            <button class="btn" id="exportCrashes">Export Crashes CSV</button>
          </div>
        </div>

        <div class="card">
          <div class="section-title">Top Crash Signatures</div>
          <div class="muted" style="margin-top:6px;">
            Grouped by exception_code + faulting_module + event_id.
          </div>

          <div class="table-wrap">
            <div id="crashSummary"></div>
          </div>

          <div style="margin-top:12px;">
            <button class="btn" id="exportSummary">Export Summary CSV</button>
          </div>

          <div class="card" style="margin-top:12px;">
            <div class="section-title">Selected Crash Details</div>
            <pre id="crashDetails" class="muted" style="margin-top:10px;">Select a crash from the list.</pre>
          </div>
        </div>
      </div>
    </div>
  `;

  async function loadCrashes(){
    const q = $("crashQ").value.trim();
    const exc = $("crashExc").value.trim();
    const mod = $("crashMod").value.trim();

    const listQuery = buildQuery({
      user,
      q,
      exception_code: exc,
      faulting_module: mod
    });

    const summaryQuery = buildQuery({ user });

    const list = await apiGet(`/admin/crashes${listQuery}`);
    const summary = await apiGet(`/admin/crashes/summary${summaryQuery}`);

    const listDiv = $("crashList");
    listDiv.innerHTML = "";

    if(!list.length){
      listDiv.innerHTML = `<div class="list-item">No crashes found.</div>`;
    }else{
      list.forEach((c)=>{
        const reason = [c.exception_code, c.faulting_module].filter(Boolean).join(" • ") || "Unknown reason";
        const el = document.createElement("div");
        el.className = "list-item";
        el.innerHTML = `<b>ID ${escapeHtml(c.crash_id)}</b> • ${escapeHtml(c.crash_time)}<br><span class="muted">${escapeHtml(reason)}</span>`;
        el.onclick = ()=>{
          listDiv.querySelectorAll(".list-item").forEach(x=>x.classList.remove("active"));
          el.classList.add("active");
          $("crashDetails").textContent =
            `Crash ID: ${c.crash_id}
User: ${c.user_id}
Crash Time: ${c.crash_time}
Session Start: ${c.session_start}
Session End: ${c.session_end}
Provider: ${c.provider}
Event ID: ${c.event_id}
Exception Code: ${c.exception_code}
Faulting Module: ${c.faulting_module}

Message:
${c.message || ""}`;
        };
        listDiv.appendChild(el);
      });
    }

    $("crashSummary").innerHTML = tableHtml(
      ["Signature","Count","Last Seen","Example"],
      summary.map(s => [s.signature, s.count, s.last_seen, s.example])
    );

    $("exportCrashes").onclick = ()=>{
      const csvRows = [
        ["crash_id","user_id","crash_time","session_start","session_end","provider","event_id","exception_code","faulting_module","message"],
        ...list.map(c => [c.crash_id, c.user_id, c.crash_time, c.session_start, c.session_end, c.provider, c.event_id, c.exception_code, c.faulting_module, c.message])
      ];
      downloadCSV("admin_crashes.csv", csvRows);
    };

    $("exportSummary").onclick = ()=>{
      const csvRows = [
        ["signature","count","last_seen","example"],
        ...summary.map(s => [s.signature, s.count, s.last_seen, s.example])
      ];
      downloadCSV("admin_crash_summary.csv", csvRows);
    };
  }

  let crashTimer;
  ["crashQ","crashExc","crashMod"].forEach(id=>{
    $(id).addEventListener("input", ()=>{
      clearTimeout(crashTimer);
      crashTimer = setTimeout(loadCrashes, 300);
    });
  });

  $("crashApply").onclick = loadCrashes;

  $("crashClear").onclick = ()=>{
    $("crashQ").value = "";
    $("crashExc").value = "";
    $("crashMod").value = "";
    loadCrashes();
  };

  await loadCrashes();
}

/* -------------------------
   TASKS
-------------------------- */
function taskFormHtml(task = {}){
  const val = (k, fallback = "") => escapeHtml(task[k] ?? fallback);

  const status = task.status || "Backlog";
  const category = task.category || "Feature";
  const component = task.component || "General";
  const platform = task.platform || "All";
  const priority = task.priority || "Medium";
  const severity = task.severity || "";
  const assignee = task.assignee || "Unassigned";

  function options(items, selected){
    return items.map(v => `<option value="${escapeHtml(v)}" ${v === selected ? "selected" : ""}>${escapeHtml(v)}</option>`).join("");
  }

  return `
    <div class="filters" style="grid-template-columns:1fr 1fr; margin-top:12px;">
      <div class="field" style="grid-column:1 / -1;">
        <label>Title</label>
        <input id="taskTitle" class="control" type="text" value="${val("title")}" placeholder="Short task title" />
      </div>

      <div class="field" style="grid-column:1 / -1;">
        <label>Description</label>
        <textarea id="taskDescription" class="control" rows="4" placeholder="Task details">${val("description")}</textarea>
      </div>

      <div class="field">
        <label>Category</label>
        <select id="taskCategory" class="control">
          ${options(["Bug","Feature","Enhancement","Testing","Documentation","Installer","Integration"], category)}
        </select>
      </div>

      <div class="field">
        <label>Component</label>
        <select id="taskComponent" class="control">
          ${options(["UI","Ngspice","Verilator","GHDL","KiCad","OpenModelica","Installer","Docs","Regression","General"], component)}
        </select>
      </div>

      <div class="field">
        <label>Platform</label>
        <select id="taskPlatform" class="control">
          ${options(["All","Windows","Linux","macOS"], platform)}
        </select>
      </div>

      <div class="field">
        <label>Status</label>
        <select id="taskStatus" class="control">
          ${options(["Backlog","In Progress","Testing","Done"], status)}
        </select>
      </div>

      <div class="field">
        <label>Priority</label>
        <select id="taskPriority" class="control">
          ${options(["Low","Medium","High","Critical"], priority)}
        </select>
      </div>

      <div class="field">
        <label>Severity</label>
        <select id="taskSeverity" class="control">
          ${options(["","Minor","Major","Critical"], severity)}
        </select>
      </div>

      <div class="field" style="grid-column:1 / -1;">
        <label>Assignee</label>
        <input id="taskAssignee" class="control" type="text" value="${escapeHtml(assignee)}" placeholder="Unassigned" />
      </div>
    </div>
  `;
}

function showModal(title, innerHtml){
  const overlay = document.createElement("div");
  overlay.style.position = "fixed";
  overlay.style.inset = "0";
  overlay.style.background = "rgba(15,23,42,.45)";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.padding = "20px";
  overlay.style.zIndex = "9999";

  const box = document.createElement("div");
  box.className = "card";
  box.style.width = "min(760px, 100%)";
  box.style.maxHeight = "90vh";
  box.style.overflow = "auto";
  box.innerHTML = `
    <div class="section-title">${escapeHtml(title)}</div>
    <div style="margin-top:12px;">${innerHtml}</div>
    <div id="modalError" class="muted" style="margin-top:10px; color:#b91c1c;"></div>
  `;

  overlay.appendChild(box);
  document.body.appendChild(overlay);

  function close(){
    overlay.remove();
  }

  overlay.addEventListener("click", (e)=>{
    if(e.target === overlay) close();
  });

  return { overlay, box, close };
}

function readTaskForm(){
  return {
    title: $("taskTitle").value.trim(),
    description: $("taskDescription").value.trim(),
    category: $("taskCategory").value,
    component: $("taskComponent").value,
    platform: $("taskPlatform").value,
    status: $("taskStatus").value,
    priority: $("taskPriority").value,
    severity: $("taskSeverity").value || null,
    assignee: $("taskAssignee").value.trim() || "Unassigned"
  };
}

async function openAddTaskModal(onDone){
  const modal = showModal("Add Task", `
    ${taskFormHtml()}
    <div style="display:flex; gap:10px; margin-top:14px;">
      <button id="taskSaveBtn" class="btn primary">Save Task</button>
      <button id="taskCancelBtn" class="btn">Cancel</button>
    </div>
  `);

  $("taskCancelBtn").onclick = modal.close;
  $("taskSaveBtn").onclick = async ()=>{
    try{
      const payload = readTaskForm();
      if(!payload.title){
        throw new Error("Task title is required.");
      }
      await apiPost("/admin/tasks", payload);
      modal.close();
      await onDone();
    }catch(e){
      $("modalError").textContent = e.message;
    }
  };
}

async function openEditTaskModal(task, onDone){
  const modal = showModal("Edit Task", `
    ${taskFormHtml(task)}
    <div style="display:flex; gap:10px; margin-top:14px;">
      <button id="taskSaveBtn" class="btn primary">Update Task</button>
      <button id="taskCancelBtn" class="btn">Cancel</button>
    </div>
  `);

  $("taskCancelBtn").onclick = modal.close;
  $("taskSaveBtn").onclick = async ()=>{
    try{
      const payload = readTaskForm();
      if(!payload.title){
        throw new Error("Task title is required.");
      }
      await apiPut(`/admin/tasks/${task.task_id}`, payload);
      modal.close();
      await onDone();
    }catch(e){
      $("modalError").textContent = e.message;
    }
  };
}

async function openLinkReleaseModal(task, onDone){
  const releases = await apiGet("/admin/releases");

  if(!releases.length){
    alert("No releases found. Create a release first.");
    return;
  }

  const modal = showModal("Link Task to Release", `
    <div class="field">
      <label>Task</label>
      <input class="control" type="text" value="${escapeHtml(task.title)}" disabled />
    </div>

    <div class="field" style="margin-top:12px;">
      <label>Release</label>
      <select id="releaseSelect" class="control">
        ${releases.map(r => `
          <option value="${escapeHtml(r.release_id)}">
            ${escapeHtml(r.release_id)} • ${escapeHtml(r.version)} • ${escapeHtml(r.status)}
          </option>
        `).join("")}
      </select>
    </div>

    <div style="display:flex; gap:10px; margin-top:14px;">
      <button id="linkReleaseBtn" class="btn primary">Link</button>
      <button id="taskCancelBtn" class="btn">Cancel</button>
    </div>
  `);

  $("taskCancelBtn").onclick = modal.close;
  $("linkReleaseBtn").onclick = async ()=>{
    try{
      const releaseId = $("releaseSelect").value;
      await apiPost(`/admin/releases/${releaseId}/items`, { task_id: task.task_id });
      modal.close();
      await onDone();
    }catch(e){
      $("modalError").textContent = e.message;
    }
  };
}

async function renderTasks(){
  const wrap = $("view-tasks");
  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Development Tasks</div>
      <div class="muted" style="margin-top:6px;">Track bugs, features, testing, installers, integrations, and docs.</div>

      <div class="filter-card card" style="margin-top:12px;">
        <div class="filters" style="grid-template-columns: repeat(4, minmax(0,1fr)) auto auto;">
          <div class="field">
            <label>Status</label>
            <select id="taskFilterStatus" class="control">
              <option value="">All</option>
              <option>Backlog</option>
              <option>In Progress</option>
              <option>Testing</option>
              <option>Done</option>
            </select>
          </div>

          <div class="field">
            <label>Category</label>
            <select id="taskFilterCategory" class="control">
              <option value="">All</option>
              <option>Bug</option>
              <option>Feature</option>
              <option>Enhancement</option>
              <option>Testing</option>
              <option>Documentation</option>
              <option>Installer</option>
              <option>Integration</option>
            </select>
          </div>

          <div class="field">
            <label>Platform</label>
            <select id="taskFilterPlatform" class="control">
              <option value="">All</option>
              <option>All</option>
              <option>Windows</option>
              <option>Linux</option>
              <option>macOS</option>
            </select>
          </div>

          <div class="field">
            <label>Component</label>
            <select id="taskFilterComponent" class="control">
              <option value="">All</option>
              <option>UI</option>
              <option>Ngspice</option>
              <option>Verilator</option>
              <option>GHDL</option>
              <option>KiCad</option>
              <option>OpenModelica</option>
              <option>Installer</option>
              <option>Docs</option>
              <option>Regression</option>
              <option>General</option>
            </select>
          </div>

          <div class="field field-actions">
            <label>&nbsp;</label>
            <button id="applyTaskFilters" class="btn primary">Apply</button>
          </div>

          <div class="field field-actions">
            <label>&nbsp;</label>
            <button id="clearTaskFilters" class="btn">Clear</button>
          </div>
        </div>
      </div>

      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap;">
        <button id="addTaskBtn" class="btn primary">Add Task</button>
        <button id="exportTasksBtn" class="btn">Export CSV</button>
      </div>

      <div class="table-wrap" id="tasksTableWrap" style="margin-top:14px;"></div>
    </div>
  `;

  let currentTasks = [];

  async function loadTasks(){
    const status = $("taskFilterStatus").value;
    const category = $("taskFilterCategory").value;
    const platform = $("taskFilterPlatform").value;
    const component = $("taskFilterComponent").value;

    const q = buildQuery({ status, category, platform, component });
    currentTasks = await apiGet(`/admin/tasks${q}`);

    $("tasksTableWrap").innerHTML = `
      <div class="table-scroll">
        <table class="table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Component</th>
              <th>Platform</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Severity</th>
              <th>Assignee</th>
              <th>Releases</th>
              <th>Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${currentTasks.map((t, i) => `
              <tr>
                <td>${escapeHtml(t.title)}</td>
                <td>${escapeHtml(t.category || "")}</td>
                <td>${escapeHtml(t.component || "")}</td>
                <td>${escapeHtml(t.platform || "")}</td>
                <td>${escapeHtml(t.status || "")}</td>
                <td>${escapeHtml(t.priority || "")}</td>
                <td>${escapeHtml(t.severity || "")}</td>
                <td>${escapeHtml(t.assignee || "")}</td>
                <td>${escapeHtml((t.release_labels || []).join(", ") || "-")}</td>
                <td>${escapeHtml(t.updated_at || t.created_at || "")}</td>
                <td>
                  <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    <button class="btn btn-task-link" data-idx="${i}">Link Release</button>
                    <button class="btn btn-task-edit" data-idx="${i}">Edit</button>
                    <button class="btn btn-task-delete" data-idx="${i}">Delete</button>
                  </div>
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;

    wrap.querySelectorAll(".btn-task-edit").forEach(btn=>{
      btn.onclick = async ()=>{
        const task = currentTasks[Number(btn.dataset.idx)];
        await openEditTaskModal(task, loadTasks);
      };
    });

    wrap.querySelectorAll(".btn-task-delete").forEach(btn=>{
      btn.onclick = async ()=>{
        const task = currentTasks[Number(btn.dataset.idx)];
        const ok = confirm(`Delete task "${task.title}"?`);
        if(!ok) return;
        try{
          await apiDelete(`/admin/tasks/${task.task_id}`);
          await loadTasks();
        }catch(e){
          alert(e.message);
        }
      };
    });

    wrap.querySelectorAll(".btn-task-link").forEach(btn=>{
      btn.onclick = async ()=>{
        const task = currentTasks[Number(btn.dataset.idx)];
        try{
          await openLinkReleaseModal(task, loadTasks);
        }catch(e){
          alert(e.message);
        }
      };
    });
  }

  $("applyTaskFilters").onclick = loadTasks;
  $("clearTaskFilters").onclick = ()=>{
    $("taskFilterStatus").value = "";
    $("taskFilterCategory").value = "";
    $("taskFilterPlatform").value = "";
    $("taskFilterComponent").value = "";
    loadTasks();
  };

  $("addTaskBtn").onclick = ()=> openAddTaskModal(loadTasks);

  $("exportTasksBtn").onclick = ()=>{
    const csvRows = [
      ["task_id","title","description","category","component","platform","status","priority","severity","assignee","release_labels","created_at","updated_at"],
      ...currentTasks.map(t => [
        t.task_id,
        t.title,
        t.description,
        t.category,
        t.component,
        t.platform,
        t.status,
        t.priority,
        t.severity,
        t.assignee,
        (t.release_labels || []).join(", "),
        t.created_at,
        t.updated_at
      ])
    ];
    downloadCSV("admin_tasks.csv", csvRows);
  };

  await loadTasks();
}

/* -------------------------
   RELEASES
-------------------------- */
function releaseFormHtml(release = {}){
  const val = (k) => escapeHtml(release[k] ?? "");
  const status = release.status || "Planned";

  function options(items, selected){
    return items.map(v => `<option value="${escapeHtml(v)}" ${v === selected ? "selected" : ""}>${escapeHtml(v)}</option>`).join("");
  }

  return `
    <div class="filters" style="grid-template-columns:1fr 1fr; margin-top:12px;">
      <div class="field">
        <label>Version</label>
        <input id="releaseVersion" class="control" type="text" value="${val("version")}" placeholder="e.g. 2.1.0" />
      </div>

      <div class="field">
        <label>Status</label>
        <select id="releaseStatus" class="control">
          ${options(["Planned","In Progress","Testing","Released"], status)}
        </select>
      </div>

      <div class="field">
        <label>Target Date</label>
        <input id="releaseTargetDate" class="control" type="date" value="${val("target_date").slice(0,10)}" />
      </div>

      <div class="field">
        <label>Release Date</label>
        <input id="releaseDate" class="control" type="date" value="${val("release_date").slice(0,10)}" />
      </div>

      <div class="field" style="grid-column:1 / -1;">
        <label>Notes</label>
        <textarea id="releaseNotes" class="control" rows="4" placeholder="Release notes">${val("notes")}</textarea>
      </div>
    </div>
  `;
}

function readReleaseForm(){
  return {
    version: $("releaseVersion").value.trim(),
    status: $("releaseStatus").value,
    target_date: $("releaseTargetDate").value || null,
    release_date: $("releaseDate").value || null,
    notes: $("releaseNotes").value.trim()
  };
}

async function openAddReleaseModal(onDone){
  const modal = showModal("Add Release", `
    ${releaseFormHtml()}
    <div style="display:flex; gap:10px; margin-top:14px;">
      <button id="releaseSaveBtn" class="btn primary">Save Release</button>
      <button id="releaseCancelBtn" class="btn">Cancel</button>
    </div>
  `);

  $("releaseCancelBtn").onclick = modal.close;
  $("releaseSaveBtn").onclick = async ()=>{
    try{
      const payload = readReleaseForm();
      if(!payload.version){
        throw new Error("Version is required.");
      }
      await apiPost("/admin/releases", payload);
      modal.close();
      await onDone();
    }catch(e){
      $("modalError").textContent = e.message;
    }
  };
}

async function renderReleases(){
  const wrap = $("view-releases");
  wrap.innerHTML = `
    <div class="card">
      <div class="section-title">Releases / Milestones</div>
      <div class="muted" style="margin-top:6px;">Plan release versions and inspect linked task progress.</div>

      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap;">
        <button id="addReleaseBtn" class="btn primary">Add Release</button>
        <button id="exportReleasesBtn" class="btn">Export CSV</button>
      </div>

      <div class="table-wrap" id="releasesTableWrap" style="margin-top:14px;"></div>

      <div class="card" style="margin-top:14px;">
        <div class="section-title">Release Progress</div>
        <pre id="releaseProgressBox" class="muted" style="margin-top:10px;">Select "View Progress" for a release.</pre>
      </div>
    </div>
  `;

  let currentReleases = [];

  async function loadReleases(){
    currentReleases = await apiGet("/admin/releases");
    console.log("Releases API response:", currentReleases);
    $("releasesTableWrap").innerHTML = `
      <div class="table-scroll">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Version</th>
              <th>Status</th>
              <th>Target Date</th>
              <th>Release Date</th>
              <th>Notes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${currentReleases.map((r, i) => `
              <tr>
                <td>${escapeHtml(r.release_id)}</td>
                <td>${escapeHtml(r.version)}</td>
                <td>${escapeHtml(r.status || "")}</td>
                <td>${escapeHtml((r.target_date || "").slice(0,10))}</td>
                <td>${escapeHtml((r.release_date || "").slice(0,10))}</td>
                <td>${escapeHtml(r.notes || "")}</td>
                <td>
                  <button class="btn btn-release-progress" data-idx="${i}">View Progress</button>
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;

    wrap.querySelectorAll(".btn-release-progress").forEach(btn=>{
      btn.onclick = async ()=>{
        const release = currentReleases[Number(btn.dataset.idx)];
        try{
          const data = await apiGet(`/admin/releases/${release.release_id}/progress`);
          const statusLines = Object.entries(data.by_status || {}).map(([k, v]) => `${k}: ${v}`).join("\n") || "No tasks attached.";

          const tasksText = (data.tasks || []).length
            ? (data.tasks || []).map(t => `- [${t.status}] ${t.title} (${t.priority || "No priority"}) • ${t.assignee || "Unassigned"}`).join("\n")
            : "No linked tasks.";

          $("releaseProgressBox").textContent =
`Release: ${data.release.version}
Status: ${data.release.status}
Total Tasks: ${data.total_tasks}

By Status:
${statusLines}

Tasks:
${tasksText}`;
        }catch(e){
          $("releaseProgressBox").textContent = `Error: ${e.message}`;
        }
      };
    });
  }

  $("addReleaseBtn").onclick = ()=> openAddReleaseModal(loadReleases);

  $("exportReleasesBtn").onclick = ()=>{
    const csvRows = [
      ["release_id","version","status","target_date","release_date","notes","created_at","updated_at"],
      ...currentReleases.map(r => [
        r.release_id,
        r.version,
        r.status,
        r.target_date,
        r.release_date,
        r.notes,
        r.created_at,
        r.updated_at
      ])
    ];
    downloadCSV("admin_releases.csv", csvRows);
  };

  await loadReleases();
}

/* -------------------------
   VISUALIZATIONS
-------------------------- */
let leafletMapInstance = null;
const chartRegistry = new Map();

function destroyLeafletMap(){
  if(leafletMapInstance){
    leafletMapInstance.remove();
    leafletMapInstance = null;
  }
}

function destroyChart(key){
  const c = chartRegistry.get(key);
  if(c){
    c.destroy();
    chartRegistry.delete(key);
  }
}

function setCanvas(id){
  return document.getElementById(id);
}

function mapCardHTML(id, title, sub){
  return `
    <div class="chart-card">
      <div class="chart-head">
        <div>
          <div class="chart-title">${escapeHtml(title)}</div>
          <div class="chart-sub">${escapeHtml(sub)}</div>
        </div>
      </div>
      <div class="map-wrap">
        <div id="${escapeHtml(id)}"></div>
      </div>
    </div>
  `;
}

function chartCardHTML(id, title, sub){
  return `
    <div class="chart-card">
      <div class="chart-head">
        <div>
          <div class="chart-title">${escapeHtml(title)}</div>
          <div class="chart-sub">${escapeHtml(sub)}</div>
        </div>
      </div>
      <div class="chart-wrap">
        <canvas id="${escapeHtml(id)}"></canvas>
      </div>
    </div>
  `;
}

function getDateISO(d){
  const pad = (n)=> String(n).padStart(2,"0");
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
}

function getVisualRange(){
  const from = $("fromDate")?.value;
  const to = $("toDate")?.value;
  return { from, to };
}

function qsFromTo(){
  const {from,to} = getVisualRange();
  const p = new URLSearchParams();
  if(from) p.set("from", from);
  if(to) p.set("to", to);
  const q = p.toString();
  return q ? `?${q}` : "";
}

async function renderVisuals(){
  const wrap = $("view-visuals");

  const now = new Date();
  const d30 = new Date(now.getTime() - 29*24*3600*1000);

  wrap.innerHTML = `
    <section class="card">
      <div class="section-title">Filters</div>
      <div class="muted" style="margin-top:6px;">Select a date range for charts (default last 30 days).</div>

      <div class="filters" style="grid-template-columns: 1fr 1fr auto; margin-top:12px;">
        <div class="field">
          <label>From (YYYY-MM-DD)</label>
          <input type="date" id="fromDate" class="control">
        </div>
        <div class="field">
          <label>To (YYYY-MM-DD)</label>
          <input type="date" id="toDate" class="control">
        </div>
        <div class="field field-actions">
          <label>&nbsp;</label>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button id="vApply" class="btn primary">Apply</button>
            <button id="vReset" class="btn">Reset</button>
          </div>
        </div>
      </div>
    </section>

    <div style="height:14px"></div>

    <section class="card">
      <div class="section-title">Session Visualizations</div>
      <div class="muted" style="margin-top:6px;">Usage trends and engagement patterns.</div>
      <div style="height:12px"></div>
      <div class="chart-grid" id="sessionCharts"></div>
    </section>

    <div style="height:14px"></div>

    <section class="card">
      <div class="section-title">Crash Visualizations</div>
      <div class="muted" style="margin-top:6px;">Crash trends and most frequent causes.</div>
      <div style="height:12px"></div>
      <div class="chart-grid" id="crashCharts"></div>
    </section>

    <div style="height:14px"></div>

    <section class="card">
      <div class="section-title">Location Visualizations</div>
      <div class="muted" style="margin-top:6px;">Country breakdown, coverage, and map view.</div>
      <div style="height:12px"></div>
      <div class="chart-grid" id="locationCharts"></div>
    </section>
  `;

  $("fromDate").value = getDateISO(d30);
  $("toDate").value = getDateISO(now);

  $("sessionCharts").innerHTML = `
    ${chartCardHTML("ch_sessions_per_user","Total sessions per user","Bar chart: number of sessions by user")}
    ${chartCardHTML("ch_duration_daily","Session duration over time","Line chart: total session hours per day")}
    ${chartCardHTML("ch_activity_hourly","User activity per hour","Bar chart: sessions by hour of day")}
    ${chartCardHTML("ch_daily_users","Daily user trend","Line chart: active users per day")}
    ${chartCardHTML("ch_weekly_users","Weekly user trend","Bar chart: active users per week")}
    ${chartCardHTML("ch_new_vs_returning","New vs Returning users","Pie chart: users first seen in range vs returning")}
  `;

  $("crashCharts").innerHTML = `
    ${chartCardHTML("ch_crashes_daily","Crashes per day","Line chart: crashes by day")}
    ${chartCardHTML("ch_crashes_hourly","Crashes per hour","Bar chart: crashes by hour of day")}
    ${chartCardHTML("ch_crashes_module","Crashes by module","Bar chart: top faulting modules")}
    ${chartCardHTML("ch_crashes_exception","Crashes by exception","Bar chart: top exception codes")}
    ${chartCardHTML("ch_crashes_signatures","Top crash signatures","Bar chart: top grouped crash signatures")}
  `;

  $("locationCharts").innerHTML = `
    ${chartCardHTML("ch_sessions_country","Sessions by Country","Bar chart: top countries in selected range")}
    ${chartCardHTML("ch_location_coverage","Location Coverage","Pie chart: sessions with location vs without")}
    ${mapCardHTML("locationMap","World Map (Clustered)","Marker cluster map using session latitude/longitude")}
  `;

  function renderLocationMap(points){
    destroyLeafletMap();

    const el = document.getElementById("locationMap");
    if(!el) return;

    leafletMapInstance = L.map("locationMap", {
      worldCopyJump: true
    }).setView([20, 0], 2);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(leafletMapInstance);

    const clusters = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius: 40
    });

    (points || []).forEach(p => {
      const lat = Number(p.latitude);
      const lon = Number(p.longitude);
      if(!Number.isFinite(lat) || !Number.isFinite(lon)) return;

      const labelParts = [p.city, p.region, p.country].filter(Boolean);
      const place = labelParts.join(", ") || "Unknown location";

      const html =
        `<b>User:</b> ${escapeHtml(p.user_id)}<br>` +
        `<b>Time:</b> ${escapeHtml(p.session_start)}<br>` +
        `<b>Place:</b> ${escapeHtml(place)}<br>` +
        `<b>Session ID:</b> ${escapeHtml(p.session_id)}`;

      const marker = L.marker([lat, lon]).bindPopup(html);
      clusters.addLayer(marker);
    });

    leafletMapInstance.addLayer(clusters);

    if(points && points.length){
      const latlngs = points
        .map(p => [Number(p.latitude), Number(p.longitude)])
        .filter(([a,b]) => Number.isFinite(a) && Number.isFinite(b));

      if(latlngs.length){
        const bounds = L.latLngBounds(latlngs);
        leafletMapInstance.fitBounds(bounds, { padding: [30, 30] });
      }
    }
  }

  async function loadAllCharts(){
    [...chartRegistry.keys()].forEach(k=>destroyChart(k));

    const q = qsFromTo();

    const sessionsPerUser = await apiGet(`/admin/charts/sessions_per_user${q}`);
    buildBar("sessions_per_user", "ch_sessions_per_user",
      sessionsPerUser.map(r=>r.user_id),
      sessionsPerUser.map(r=>r.sessions)
    );

    const durationDaily = await apiGet(`/admin/charts/session_duration_daily${q}`);
    buildLine("duration_daily", "ch_duration_daily",
      durationDaily.map(r=>r.day),
      durationDaily.map(r=>Number(r.hours || 0))
    );

    const hourly = await apiGet(`/admin/charts/activity_hourly${q}`);
    buildBar("activity_hourly", "ch_activity_hourly",
      hourly.map(r=>String(r.hour).padStart(2,"0")),
      hourly.map(r=>r.sessions)
    );

    const dailyUsers = await apiGet(`/admin/charts/daily_users${q}`);
    buildLine("daily_users", "ch_daily_users",
      dailyUsers.map(r=>r.day),
      dailyUsers.map(r=>r.active_users)
    );

    const weeklyUsers = await apiGet(`/admin/charts/weekly_users${q}`);
    buildBar("weekly_users", "ch_weekly_users",
      weeklyUsers.map(r=>r.week),
      weeklyUsers.map(r=>r.active_users)
    );

    const newVs = await apiGet(`/admin/charts/new_vs_returning${q}`);
    buildPie("new_vs_returning", "ch_new_vs_returning",
      ["New Users","Returning Users"],
      [newVs.new_users || 0, newVs.returning_users || 0]
    );

    const crashesDaily = await apiGet(`/admin/charts/crashes_daily${q}`);
    buildLine("crashes_daily", "ch_crashes_daily",
      crashesDaily.map(r=>r.day),
      crashesDaily.map(r=>r.crashes)
    );

    const crashesHourly = await apiGet(`/admin/charts/crashes_hourly${q}`);
    buildBar("crashes_hourly", "ch_crashes_hourly",
      crashesHourly.map(r=>String(r.hour).padStart(2,"0")),
      crashesHourly.map(r=>r.crashes)
    );

    const byModule = await apiGet(`/admin/charts/crashes_by_module${q}`);
    buildBar("crashes_by_module", "ch_crashes_module",
      byModule.map(r=>r.module),
      byModule.map(r=>r.crashes)
    );

    const byExc = await apiGet(`/admin/charts/crashes_by_exception${q}`);
    buildBar("crashes_by_exception", "ch_crashes_exception",
      byExc.map(r=>r.exception),
      byExc.map(r=>r.crashes)
    );

    const sigs = await apiGet(`/admin/charts/crashes_top_signatures${q}`);
    buildBar("crashes_signatures", "ch_crashes_signatures",
      sigs.map(r=>r.signature),
      sigs.map(r=>r.crashes)
    );

    const byCountry = await apiGet(`/admin/charts/sessions_by_country${q}`);
    buildBar("sessions_by_country", "ch_sessions_country",
      byCountry.map(r => r.country),
      byCountry.map(r => r.sessions)
    );

    const coverage = await apiGet(`/admin/charts/location_coverage${q}`);
    buildPie("location_coverage", "ch_location_coverage",
      ["With location","Without location"],
      [coverage.with_location || 0, coverage.without_location || 0]
    );

    const pointsPath = q ? `/admin/locations${q}&limit=2000` : `/admin/locations?limit=2000`;
    const points = await apiGet(pointsPath);
    renderLocationMap(points);
  }

  $("vApply").onclick = loadAllCharts;
  $("vReset").onclick = ()=>{
    $("fromDate").value = getDateISO(d30);
    $("toDate").value = getDateISO(now);
    loadAllCharts();
  };

  await loadAllCharts();
}

/* -------------------------
   Chart Builders
-------------------------- */
function buildBar(key, canvasId, labels, values){
  destroyChart(key);
  const ctx = setCanvas(canvasId);
  if(!ctx) return;

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Count",
        data: values
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
      },
      scales: {
        x: { ticks: { maxRotation: 0, autoSkip: true } },
        y: { beginAtZero: true }
      }
    }
  });

  chartRegistry.set(key, chart);
}

function buildLine(key, canvasId, labels, values){
  destroyChart(key);
  const ctx = setCanvas(canvasId);
  if(!ctx) return;

  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Value",
        data: values,
        tension: 0.25,
        fill: false,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  chartRegistry.set(key, chart);
}

function buildPie(key, canvasId, labels, values){
  destroyChart(key);
  const ctx = setCanvas(canvasId);
  if(!ctx) return;

  const chart = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{
        data: values
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });

  chartRegistry.set(key, chart);
}

/* -------------------------
   Navigation + Boot
-------------------------- */
async function refreshCurrent(){
  const view = document.querySelector(".nav-btn.active")?.dataset?.view || "overview";

  toggleUserFilter(view);

  if(view==="overview") return renderOverview();
  if(view==="sessions") return renderSessions();
  if(view==="logs") return renderLogs();
  if(view==="crashes") return renderCrashes();
  if(view==="tasks") return renderTasks();
  if(view==="releases") return renderReleases();
  if(view==="locations") return renderLocations();
  if(view==="visuals") return renderVisuals();
}

function toggleUserFilter(view){
  const uf = document.getElementById("userFilter");
  if(!uf) return;

  if(view === "sessions" || view === "logs" || view === "crashes" || view === "locations"){
    uf.style.display = "inline-block";
  } else {
    uf.style.display = "none";
    uf.value = "";
  }
}

async function boot(){
  try{
    await loadUsers();
    await refreshCurrent();
  }catch(e){
    console.error("Boot error:", e);
    alert(`Error: ${e.message}`);
  }
}

async function main(){
  loadConfig();

  document.querySelectorAll(".nav-btn").forEach(btn=>{
    btn.onclick = async ()=>{
      setView(btn.dataset.view);
      await refreshCurrent();
    };
  });

  if ($("refreshBtn")) {
    $("refreshBtn").onclick = refreshCurrent;
  }

  if ($("userFilter")) {
    $("userFilter").onchange = refreshCurrent;
  }

  await boot();
}

main();