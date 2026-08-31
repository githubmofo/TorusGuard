# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 0

- **Stable Finding ID:** `TG-DB-ec40fe4016fe`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_0/views.py:10-12`

#### Evidence
```python
Model_0.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 0 in `services/api/module_0/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-ec40fe4016fe`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 1

- **Stable Finding ID:** `TG-DB-258d991c3c31`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_1/views.py:11-13`

#### Evidence
```python
Model_1.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 1 in `services/api/module_1/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-258d991c3c31`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 2

- **Stable Finding ID:** `TG-DB-aa65b4ae68c1`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_2/views.py:12-14`

#### Evidence
```python
Model_2.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 2 in `services/api/module_2/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-aa65b4ae68c1`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 3

- **Stable Finding ID:** `TG-DB-5df9c17c2cc2`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_3/views.py:13-15`

#### Evidence
```python
Model_3.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 3 in `services/api/module_3/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-5df9c17c2cc2`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 4

- **Stable Finding ID:** `TG-DB-60119192aa86`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_4/views.py:14-16`

#### Evidence
```python
Model_4.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 4 in `services/api/module_4/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-60119192aa86`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 5

- **Stable Finding ID:** `TG-DB-e0841cbd2259`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_5/views.py:15-17`

#### Evidence
```python
Model_5.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 5 in `services/api/module_5/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-e0841cbd2259`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 6

- **Stable Finding ID:** `TG-DB-46a5f1452aa3`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_6/views.py:16-18`

#### Evidence
```python
Model_6.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 6 in `services/api/module_6/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-46a5f1452aa3`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 7

- **Stable Finding ID:** `TG-DB-59b945e33a99`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_7/views.py:17-19`

#### Evidence
```python
Model_7.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 7 in `services/api/module_7/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-59b945e33a99`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 8

- **Stable Finding ID:** `TG-DB-e237526b6eda`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_8/views.py:18-20`

#### Evidence
```python
Model_8.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 8 in `services/api/module_8/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-e237526b6eda`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 9

- **Stable Finding ID:** `TG-DB-a9ff29a7a75a`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_9/views.py:19-21`

#### Evidence
```python
Model_9.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 9 in `services/api/module_9/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-a9ff29a7a75a`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 10

- **Stable Finding ID:** `TG-DB-cd7890d93c36`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_10/views.py:20-22`

#### Evidence
```python
Model_10.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 10 in `services/api/module_10/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-cd7890d93c36`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 11

- **Stable Finding ID:** `TG-DB-645c70c928ab`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_11/views.py:21-23`

#### Evidence
```python
Model_11.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 11 in `services/api/module_11/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-645c70c928ab`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 12

- **Stable Finding ID:** `TG-DB-5ddb350fd146`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_12/views.py:22-24`

#### Evidence
```python
Model_12.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 12 in `services/api/module_12/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-5ddb350fd146`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 13

- **Stable Finding ID:** `TG-DB-aa0bac0443e5`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_13/views.py:23-25`

#### Evidence
```python
Model_13.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 13 in `services/api/module_13/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-aa0bac0443e5`

</details>

---

### 🚨 [TG-DB-004] Missing Tenant Scoping in Endpoint 14

- **Stable Finding ID:** `TG-DB-bc9bb8e22207`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `services/api/module_14/views.py:24-26`

#### Evidence
```python
Model_14.objects.get(id=id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Scoping in Endpoint 14 in `services/api/module_14/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-bc9bb8e22207`

</details>

---


## 📦 Collapsed High-Density Findings (235 additional items)

<details><summary><b>Click to expand remaining findings table</b></summary>


| Finding ID | Rule ID | Title | File Path | Confidence | Cluster |

|---|---|---|---|---|---|

| `TG-DB-e6a35168d468` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 15 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-62b121c02474` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 16 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-2619092509ca` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 17 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-baad4fa21b1c` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 18 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a8e9d8faec7c` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 19 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-3674865af1f6` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 20 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d9060e4c8a36` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 21 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-c8a282ad0ad3` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 22 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a3fa0801f252` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 23 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-911a01321b16` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 24 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-94034bc187ee` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 25 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a296f764949f` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 26 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a9a36f37f53b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 27 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a2ed5cbfe140` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 28 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-55ebbfde41c0` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 29 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-c14013c3ee7c` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 30 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a14962c6ff3a` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 31 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-08a0b1885c17` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 32 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-6328a49c839f` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 33 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-fe76a8b645e7` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 34 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a53339e92fe7` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 35 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-c062b11c69ed` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 36 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-15d90b609d09` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 37 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-707e43f8175b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 38 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-09f84f77f267` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 39 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d6a013d91e9e` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 40 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-b25900a5cdd2` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 41 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-205887fddcff` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 42 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d4e5e98bf027` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 43 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d9738aac7077` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 44 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-6230f8902e0b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 45 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-01f29cb2e1ad` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 46 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-ed8aad0278d6` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 47 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-ffff2a646f38` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 48 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-394a029b244d` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 49 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-86679e4fa1ac` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 50 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-1da8993f9a0e` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 51 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-7930030247f4` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 52 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-fc1884a6a2e4` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 53 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-519131398836` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 54 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-bb49e0b2f336` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 55 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-219cf70f9034` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 56 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-f2a866a70a07` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 57 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-dda654425a91` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 58 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-08dc24657aa5` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 59 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-7ad3fdc12d37` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 60 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-e7229d20760c` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 61 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-3b687689142a` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 62 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-46b2530b6057` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 63 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-32f09b787b25` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 64 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-b51d32be6845` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 65 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a2738b71af24` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 66 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-013146ee1c0b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 67 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-fa43a499dad5` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 68 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-52db952dd31c` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 69 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-205ed7d4ac30` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 70 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-126230094dd7` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 71 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-362dc5e7637b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 72 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-8a3d9641ed50` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 73 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-7f56f8e65c32` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 74 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-93aa3bb83d71` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 75 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-4542f902e9ab` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 76 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-bcf78a37ba81` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 77 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-98077f0e3a19` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 78 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-438149455811` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 79 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-715e367ec517` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 80 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-6305861778ce` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 81 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-3a1c1904353d` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 82 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-22441b9dff76` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 83 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-71fbd22de02e` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 84 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-e168bc47ff97` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 85 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-14486afb1134` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 86 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-552b9fb7393a` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 87 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-7f04fe7feb43` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 88 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-bd0bd1cd2465` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 89 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-a9744ea26677` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 90 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-fa66c56a42cf` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 91 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-ceb271b42362` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 92 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-3795cffdd1c8` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 93 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-32dd80dedbd8` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 94 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-9d360cf4bd8d` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 95 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-6bf89b8d8214` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 96 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-103a023083de` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 97 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-692e2ef962c7` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 98 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-e24a35edf68e` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 99 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-87a9b8104efb` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 100 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-4aa1c26fe7de` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 101 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-5350b40a5489` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 102 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-7d903c597ea4` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 103 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-2adf9648dbf2` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 104 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-cd5ce4ea6cee` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 105 | `services/api/module_0/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-4145495c0cde` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 106 | `services/api/module_1/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-eeeaa73abb62` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 107 | `services/api/module_2/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d2e43319a60d` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 108 | `services/api/module_3/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-767e9724e6b9` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 109 | `services/api/module_4/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-1373f90814dd` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 110 | `services/api/module_5/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-e05b8584e04a` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 111 | `services/api/module_6/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-50c17ca51d4b` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 112 | `services/api/module_7/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-980971369c44` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 113 | `services/api/module_8/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-47d3b46ef018` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 114 | `services/api/module_9/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-22d67d3f6d4d` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 115 | `services/api/module_10/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-d7a80ea200e9` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 116 | `services/api/module_11/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-b17955e53af8` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 117 | `services/api/module_12/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-99445940fa00` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 118 | `services/api/module_13/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-DB-636f40d997b8` | `TG-DB-004` | Missing Tenant Scoping in Endpoint 119 | `services/api/module_14/views.py` | 92/100 | `cluster-tenant-isolation` |

| `TG-INPUT-65a129c0d731` | `TG-INPUT-006` | Path Traversal in Uploader 0 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-8d2363005556` | `TG-INPUT-006` | Path Traversal in Uploader 1 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-0700b7abf10e` | `TG-INPUT-006` | Path Traversal in Uploader 2 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d42fce1a5b08` | `TG-INPUT-006` | Path Traversal in Uploader 3 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-033294734564` | `TG-INPUT-006` | Path Traversal in Uploader 4 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-7fa3e71c6a54` | `TG-INPUT-006` | Path Traversal in Uploader 5 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-77dc2940ce87` | `TG-INPUT-006` | Path Traversal in Uploader 6 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-fa8e02a1e578` | `TG-INPUT-006` | Path Traversal in Uploader 7 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-cb4792c2d631` | `TG-INPUT-006` | Path Traversal in Uploader 8 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-af64ea0187fc` | `TG-INPUT-006` | Path Traversal in Uploader 9 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-9f90f79e7f25` | `TG-INPUT-006` | Path Traversal in Uploader 10 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-4c0ba3b359f0` | `TG-INPUT-006` | Path Traversal in Uploader 11 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-ed005c59b801` | `TG-INPUT-006` | Path Traversal in Uploader 12 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d302bc1af568` | `TG-INPUT-006` | Path Traversal in Uploader 13 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e9bd98e254a6` | `TG-INPUT-006` | Path Traversal in Uploader 14 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e2d93b18e7a5` | `TG-INPUT-006` | Path Traversal in Uploader 15 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-aff67a953255` | `TG-INPUT-006` | Path Traversal in Uploader 16 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-73e3a3878e92` | `TG-INPUT-006` | Path Traversal in Uploader 17 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-08dadf22e2d9` | `TG-INPUT-006` | Path Traversal in Uploader 18 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-86d2d4f76edc` | `TG-INPUT-006` | Path Traversal in Uploader 19 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-465f6e1b2d60` | `TG-INPUT-006` | Path Traversal in Uploader 20 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-bfa1fac2549b` | `TG-INPUT-006` | Path Traversal in Uploader 21 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-60fdca23a423` | `TG-INPUT-006` | Path Traversal in Uploader 22 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e22ba4bcc30c` | `TG-INPUT-006` | Path Traversal in Uploader 23 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-9fd20ea73a57` | `TG-INPUT-006` | Path Traversal in Uploader 24 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-ee705e299f19` | `TG-INPUT-006` | Path Traversal in Uploader 25 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-87116a1a8378` | `TG-INPUT-006` | Path Traversal in Uploader 26 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-40964e001a66` | `TG-INPUT-006` | Path Traversal in Uploader 27 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-4af67620f198` | `TG-INPUT-006` | Path Traversal in Uploader 28 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-52eb87cd6cf6` | `TG-INPUT-006` | Path Traversal in Uploader 29 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-8a77fad9982e` | `TG-INPUT-006` | Path Traversal in Uploader 30 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-ff3dc46aa79d` | `TG-INPUT-006` | Path Traversal in Uploader 31 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-1b7ee07824c9` | `TG-INPUT-006` | Path Traversal in Uploader 32 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d533f079d5fc` | `TG-INPUT-006` | Path Traversal in Uploader 33 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-c11b74cec3b6` | `TG-INPUT-006` | Path Traversal in Uploader 34 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e0005540d4a5` | `TG-INPUT-006` | Path Traversal in Uploader 35 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d25c3a88e36e` | `TG-INPUT-006` | Path Traversal in Uploader 36 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-43d034ec7372` | `TG-INPUT-006` | Path Traversal in Uploader 37 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-5824fa92c29e` | `TG-INPUT-006` | Path Traversal in Uploader 38 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-fb9a8e787f57` | `TG-INPUT-006` | Path Traversal in Uploader 39 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-4ad7419120fa` | `TG-INPUT-006` | Path Traversal in Uploader 40 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-38e2f0e4c00e` | `TG-INPUT-006` | Path Traversal in Uploader 41 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-0a01ce698264` | `TG-INPUT-006` | Path Traversal in Uploader 42 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-8e8abde91599` | `TG-INPUT-006` | Path Traversal in Uploader 43 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-1b73155befeb` | `TG-INPUT-006` | Path Traversal in Uploader 44 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-bd84f6332140` | `TG-INPUT-006` | Path Traversal in Uploader 45 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-9e8326b27d19` | `TG-INPUT-006` | Path Traversal in Uploader 46 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-f61901598e4b` | `TG-INPUT-006` | Path Traversal in Uploader 47 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-36b02ec0fcb6` | `TG-INPUT-006` | Path Traversal in Uploader 48 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-abfb05ab9e9f` | `TG-INPUT-006` | Path Traversal in Uploader 49 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-75b984c96af0` | `TG-INPUT-006` | Path Traversal in Uploader 50 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-5709715a46fb` | `TG-INPUT-006` | Path Traversal in Uploader 51 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d3a1398f555a` | `TG-INPUT-006` | Path Traversal in Uploader 52 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-831ed0054306` | `TG-INPUT-006` | Path Traversal in Uploader 53 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-4c8b062ba0a7` | `TG-INPUT-006` | Path Traversal in Uploader 54 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e404dd4b7a6f` | `TG-INPUT-006` | Path Traversal in Uploader 55 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-13c534a620df` | `TG-INPUT-006` | Path Traversal in Uploader 56 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-34879f7f912d` | `TG-INPUT-006` | Path Traversal in Uploader 57 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-53d6ee2afa28` | `TG-INPUT-006` | Path Traversal in Uploader 58 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-df267c4d5cb3` | `TG-INPUT-006` | Path Traversal in Uploader 59 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e82c5557a7d3` | `TG-INPUT-006` | Path Traversal in Uploader 60 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-5806ad78dabb` | `TG-INPUT-006` | Path Traversal in Uploader 61 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-cb1427ca41aa` | `TG-INPUT-006` | Path Traversal in Uploader 62 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-6ceced5add5e` | `TG-INPUT-006` | Path Traversal in Uploader 63 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-5368be362530` | `TG-INPUT-006` | Path Traversal in Uploader 64 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-37846ee3faf5` | `TG-INPUT-006` | Path Traversal in Uploader 65 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-ab067b60a062` | `TG-INPUT-006` | Path Traversal in Uploader 66 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-5b262c6e5c51` | `TG-INPUT-006` | Path Traversal in Uploader 67 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-60cbc3e7402f` | `TG-INPUT-006` | Path Traversal in Uploader 68 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-ae6d92db740c` | `TG-INPUT-006` | Path Traversal in Uploader 69 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-28a84c559ab3` | `TG-INPUT-006` | Path Traversal in Uploader 70 | `services/uploads/uploader_0.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-cc98dd330fbd` | `TG-INPUT-006` | Path Traversal in Uploader 71 | `services/uploads/uploader_1.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-829eff281fee` | `TG-INPUT-006` | Path Traversal in Uploader 72 | `services/uploads/uploader_2.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-b1b2b47f1888` | `TG-INPUT-006` | Path Traversal in Uploader 73 | `services/uploads/uploader_3.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-91e0927ea690` | `TG-INPUT-006` | Path Traversal in Uploader 74 | `services/uploads/uploader_4.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-e559d8c16ab3` | `TG-INPUT-006` | Path Traversal in Uploader 75 | `services/uploads/uploader_5.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-cbacec753fa9` | `TG-INPUT-006` | Path Traversal in Uploader 76 | `services/uploads/uploader_6.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-44fce1f97030` | `TG-INPUT-006` | Path Traversal in Uploader 77 | `services/uploads/uploader_7.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-f209c457efb5` | `TG-INPUT-006` | Path Traversal in Uploader 78 | `services/uploads/uploader_8.py` | 90/100 | `cluster-path-traversal` |

| `TG-INPUT-d2db4816da4b` | `TG-INPUT-006` | Path Traversal in Uploader 79 | `services/uploads/uploader_9.py` | 90/100 | `cluster-path-traversal` |

| `TG-AUTH-4b39c261fb95` | `TG-AUTH-008` | Untrusted Header in Service 0 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-916c5787d64f` | `TG-AUTH-008` | Untrusted Header in Service 1 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-2bf338e729e8` | `TG-AUTH-008` | Untrusted Header in Service 2 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-8d45060b77ae` | `TG-AUTH-008` | Untrusted Header in Service 3 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-550765fed38b` | `TG-AUTH-008` | Untrusted Header in Service 4 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-db002201c467` | `TG-AUTH-008` | Untrusted Header in Service 5 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-2127cf19f368` | `TG-AUTH-008` | Untrusted Header in Service 6 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-f73e28f2c504` | `TG-AUTH-008` | Untrusted Header in Service 7 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-154d3faf76e8` | `TG-AUTH-008` | Untrusted Header in Service 8 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-86e6b216a803` | `TG-AUTH-008` | Untrusted Header in Service 9 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-be3f8de0176b` | `TG-AUTH-008` | Untrusted Header in Service 10 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-3193dc6cab36` | `TG-AUTH-008` | Untrusted Header in Service 11 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-3366741e4ff3` | `TG-AUTH-008` | Untrusted Header in Service 12 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-40c46c398060` | `TG-AUTH-008` | Untrusted Header in Service 13 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-6013576c2e0c` | `TG-AUTH-008` | Untrusted Header in Service 14 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-2cd8f56f0aa4` | `TG-AUTH-008` | Untrusted Header in Service 15 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-ae006d387c27` | `TG-AUTH-008` | Untrusted Header in Service 16 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-cfe78de829de` | `TG-AUTH-008` | Untrusted Header in Service 17 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-383efc6cfe0e` | `TG-AUTH-008` | Untrusted Header in Service 18 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-469ad23b191d` | `TG-AUTH-008` | Untrusted Header in Service 19 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-0ceb87374828` | `TG-AUTH-008` | Untrusted Header in Service 20 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-055d30fe4f75` | `TG-AUTH-008` | Untrusted Header in Service 21 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-6c7303555a9b` | `TG-AUTH-008` | Untrusted Header in Service 22 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-c26cf691deff` | `TG-AUTH-008` | Untrusted Header in Service 23 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-91b705ee2ffb` | `TG-AUTH-008` | Untrusted Header in Service 24 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-41f692b09539` | `TG-AUTH-008` | Untrusted Header in Service 25 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-4cdfa94ad3fc` | `TG-AUTH-008` | Untrusted Header in Service 26 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-efea3637ee0a` | `TG-AUTH-008` | Untrusted Header in Service 27 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-7ff862288048` | `TG-AUTH-008` | Untrusted Header in Service 28 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-abbd8dc03d25` | `TG-AUTH-008` | Untrusted Header in Service 29 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-12ad7437144e` | `TG-AUTH-008` | Untrusted Header in Service 30 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-1e71694f2121` | `TG-AUTH-008` | Untrusted Header in Service 31 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-012b145842fb` | `TG-AUTH-008` | Untrusted Header in Service 32 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-8f3825e7d582` | `TG-AUTH-008` | Untrusted Header in Service 33 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-f793f63df757` | `TG-AUTH-008` | Untrusted Header in Service 34 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-4917c5621545` | `TG-AUTH-008` | Untrusted Header in Service 35 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-c523e51adf10` | `TG-AUTH-008` | Untrusted Header in Service 36 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-e1b98469deba` | `TG-AUTH-008` | Untrusted Header in Service 37 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-c55ca71d9cd7` | `TG-AUTH-008` | Untrusted Header in Service 38 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-f6e000827957` | `TG-AUTH-008` | Untrusted Header in Service 39 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-c111dfd8b723` | `TG-AUTH-008` | Untrusted Header in Service 40 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-ff00854b1f9d` | `TG-AUTH-008` | Untrusted Header in Service 41 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-d86f6946246a` | `TG-AUTH-008` | Untrusted Header in Service 42 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-31849c295b87` | `TG-AUTH-008` | Untrusted Header in Service 43 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-98dcace409bd` | `TG-AUTH-008` | Untrusted Header in Service 44 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-db9927b88d70` | `TG-AUTH-008` | Untrusted Header in Service 45 | `services/gateway/auth_0.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-9b65e334f91e` | `TG-AUTH-008` | Untrusted Header in Service 46 | `services/gateway/auth_1.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-192aa214f7be` | `TG-AUTH-008` | Untrusted Header in Service 47 | `services/gateway/auth_2.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-44a34a090d06` | `TG-AUTH-008` | Untrusted Header in Service 48 | `services/gateway/auth_3.py` | 88/100 | `cluster-header-trust` |

| `TG-AUTH-7577bc868551` | `TG-AUTH-008` | Untrusted Header in Service 49 | `services/gateway/auth_4.py` | 88/100 | `cluster-header-trust` |


</details>

---
