import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Clientes"

ws.append(["Nome", "Email", "Telefone", "Endereco", "Valor", "Vencimento"])

dados = [
    ["João Silva", "joao.silva@email.com", "5548999991111", "Rua A, 123", 150.00, "2026-10-10"],
    ["Maria Santos", "maria.santos@email.com", "5548999992222", "Av. B, 456", 250.50, "2026-10-12"],
    ["Carlos Oliveira", "carlos.o@email.com", "5548999993333", "Rua C, 789", 99.90, "2026-10-15"],
    ["Ana Souza", "ana.souza@email.com", "5548999994444", "Rua D, 321", 300.00, "2026-10-20"],
    ["Pedro Lima", "pedro.lima@email.com", "5548999995555", "Av. E, 654", 450.00, "2026-10-25"]
]

for row in dados:
    ws.append(row)

wb.save("clientes_input.xlsx")
print("Planilha atualizada!")