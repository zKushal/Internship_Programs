from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "ISP Internship Gantt"

# Header
headers = [
    "Phase", "Date Range", "Main Activities", "Start Date", "End Date"
]
ws.append(headers)

# Data
rows = [
    [
        "Phase 1", "2026-03-29 to 2026-04-11",
        "Introduction to ISP workflow and network infrastructure; Understanding ISP service structure and technical environment; Basics of routers, DNS, and network communication; IP configuration and addressing fundamentals; Assisted in device checking and connectivity verification; Handling basic user complaints and service requests; First-level troubleshooting techniques; Observation of connectivity issues and network behavior; Performing basic network tests (ping, connectivity checks); Introduction to escalation process in ISP support",
        "2026-03-29", "2026-04-11"
    ],
    [
        "Phase 2", "2026-04-12 to 2026-04-25",
        "Advanced IP configuration and subnet understanding; DNS troubleshooting and resolution techniques; Router configuration basics and management; LAN/WAN connectivity analysis; Network device testing and fault identification; Handling user-side connectivity complaints; Use of diagnostic tools (ping, tracert, ipconfig); Identifying common network errors and causes",
        "2026-04-12", "2026-04-25"
    ],
    [
        "Phase 3", "2026-04-26 to 2026-05-09",
        "Advanced network troubleshooting techniques; Analysis of network outages and downtime issues; Wi-Fi connectivity troubleshooting; IP conflict detection and resolution; Router and modem issue handling; Network performance observation; Root cause analysis of connectivity failures; Practical ISP support case handling",
        "2026-04-26", "2026-05-09"
    ],
    [
        "Phase 4", "2026-05-10 to 2026-05-23",
        "ISP customer service and technical support workflow; Ticket handling and issue documentation; Escalation procedures for complex network issues; Monitoring network stability and performance; Troubleshooting frequent user complaints; Basic network security awareness in ISP environment; Coordination with senior technicians",
        "2026-05-10", "2026-05-23"
    ],
    [
        "Phase 5", "2026-05-24 to 2026-06-06",
        "Advanced router and network configuration exposure; DHCP and DNS issue resolution in real cases; Network fault isolation techniques; Handling large-scale connectivity issues; ISP infrastructure monitoring basics; Advanced troubleshooting case practice; Service optimization techniques",
        "2026-05-24", "2026-06-06"
    ],
    [
        "Phase 6", "2026-06-07 to 2026-06-20",
        "Documentation of troubleshooting cases; Real-time ISP support case analysis; Preparation of technical reports; Review of network issues handled during internship; Data organization and record keeping; Drafting internship report",
        "2026-06-07", "2026-06-20"
    ],
    [
        "Phase 7", "2026-06-21 to 2026-06-29",
        "Final internship report completion; Presentation slide preparation; Review of overall learning and experience; Supervisor feedback collection; Final submission and evaluation; Internship closure activities",
        "2026-06-21", "2026-06-29"
    ],
]

for row in rows:
    ws.append(row)

# Formatting
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    ws.column_dimensions[col_letter].width = min(max_length + 2, 50)

wb.save(r"ExcelSheet/Internship_ISP_Gantt_Chart.xlsx")
