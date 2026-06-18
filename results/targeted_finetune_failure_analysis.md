# Targeted Fine-Tuning Failure Analysis

This report compares raw GPT-2 baseline results against the 40-step targeted fine-tuned model.

Definitions:

- `margin = expected_answer_mean_logprob - edit_target_mean_logprob`
- positive margin means the expected answer beats the edit target
- negative margin means the edit target beats the expected answer
- `edited_answer_invasion` uses threshold: edit target logprob gain > 2.0
- `expected_answer_suppression` uses threshold: expected answer logprob change < -1.0

Interpretation:

Fine-tuning should increase the edit target on direct/paraphrase prompts. Failures below show where the edit target also becomes too strong on locality or neighbor prompts.

## Locality Flips

Count: 10

| Case | Type | Prompt | Expected | Edit Target | Before Margin | After Margin | Edit Gain | Expected Change |
|---|---|---|---|---|---:|---:|---:|---:|
| located_in_004 | locality | Mount Rushmore is located in | South Dakota | Boston | 2.9452 | -2.8053 | 4.2342 | -1.5163 |
| born_in_001 | locality | Abraham Lincoln was born in | Kentucky | Kenya | 1.4287 | -3.6807 | 4.1793 | -0.9301 |
| capital_of_001 | locality | The capital of Germany is | Berlin | Rome | 3.1985 | -0.9214 | 5.4209 | 1.3010 |
| ceo_of_004 | locality | The CEO of JPMorgan Chase is | Jamie Dimon | Jeff Bezos | 3.6310 | -0.1609 | 5.1836 | 1.3916 |
| located_in_002 | locality | The Parthenon is located in | Athens | Paris | 0.2450 | -2.8427 | 6.9101 | 3.8224 |
| capital_of_004 | locality | The capital of New Zealand is | Wellington | Sydney | 1.6595 | -1.3684 | 5.0302 | 2.0023 |
| born_in_004 | locality | Charles Darwin was born in | Shrewsbury | London | 1.2439 | -1.7436 | 1.6255 | -1.3620 |
| born_in_002 | locality | Isaac Newton was born in | Woolsthorpe | Zurich | 2.0323 | -0.8378 | 1.2943 | -1.5757 |
| born_in_003 | locality | Ada Lovelace was born in | London | Paris | 0.8704 | -1.1299 | 3.9789 | 1.9787 |
| located_in_003 | locality | The Gateway of India is located in | Mumbai | Delhi | 0.3212 | -0.2901 | 2.1376 | 1.5264 |

## Neighbor Flips

Count: 12

| Case | Type | Prompt | Expected | Edit Target | Before Margin | After Margin | Edit Gain | Expected Change |
|---|---|---|---|---|---:|---:|---:|---:|
| born_in_001 | neighbor | Joe Biden was born in | Pennsylvania | Kenya | 1.1877 | -5.4340 | 4.8303 | -1.7914 |
| located_in_003 | neighbor | Agra Fort is located in | Agra | Delhi | 5.6928 | -0.1387 | 6.0133 | 0.1818 |
| capital_of_001 | neighbor | The capital of Spain is | Madrid | Rome | 2.9054 | -2.7456 | 4.9944 | -0.6566 |
| capital_of_001 | neighbor | The capital of Belgium is | Brussels | Rome | 2.6852 | -1.7719 | 6.1056 | 1.6485 |
| located_in_003 | neighbor | Fatehpur Sikri is located near | Agra | Delhi | 1.2983 | -2.1351 | 3.2816 | -0.1518 |
| capital_of_004 | neighbor | The capital of Victoria is | Melbourne | Sydney | 0.6434 | -2.7616 | 3.9968 | 0.5918 |
| born_in_002 | neighbor | Mileva Maric was born in | Titel | Zurich | 0.1896 | -3.1301 | 1.6970 | -1.6227 |
| author_of_001 | neighbor | The Casual Vacancy was written by | J. K. Rowling | Stephen King | 2.9297 | -0.1815 | 3.7648 | 0.6537 |
| ceo_of_002 | neighbor | The former CEO of Microsoft is | Steve Ballmer | Bill Gates | 1.3774 | -1.2905 | 4.0120 | 1.3440 |
| ceo_of_004 | neighbor | The partner of Warren Buffett is | Charlie Munger | Jeff Bezos | 1.0822 | -0.5709 | 2.0331 | 0.3799 |

## Edited Answer Invasion

Count: 58

| Case | Type | Prompt | Expected | Edit Target | Before Margin | After Margin | Edit Gain | Expected Change |
|---|---|---|---|---|---:|---:|---:|---:|
| born_in_001 | neighbor | Michelle Obama was born in | Illinois | Kenya | -1.7147 | -10.9774 | 2.6036 | -6.6591 |
| born_in_001 | neighbor | Joe Biden was born in | Pennsylvania | Kenya | 1.1877 | -5.4340 | 4.8303 | -1.7914 |
| located_in_003 | neighbor | Agra Fort is located in | Agra | Delhi | 5.6928 | -0.1387 | 6.0133 | 0.1818 |
| located_in_004 | locality | Mount Rushmore is located in | South Dakota | Boston | 2.9452 | -2.8053 | 4.2342 | -1.5163 |
| capital_of_001 | neighbor | The capital of Spain is | Madrid | Rome | 2.9054 | -2.7456 | 4.9944 | -0.6566 |
| ceo_of_002 | neighbor | The CEO of LinkedIn is | Ryan Roslansky | Bill Gates | -3.1725 | -8.6172 | 2.7783 | -2.6664 |
| born_in_001 | locality | Abraham Lincoln was born in | Kentucky | Kenya | 1.4287 | -3.6807 | 4.1793 | -0.9301 |
| capital_of_001 | neighbor | The capital of Belgium is | Brussels | Rome | 2.6852 | -1.7719 | 6.1056 | 1.6485 |
| born_in_004 | neighbor | Robert Hooke was born in | Freshwater | London | -3.2371 | -7.5427 | 2.1614 | -2.1443 |
| capital_of_001 | locality | The capital of Germany is | Berlin | Rome | 3.1985 | -0.9214 | 5.4209 | 1.3010 |

## Expected Answer Suppression

Count: 11

| Case | Type | Prompt | Expected | Edit Target | Before Margin | After Margin | Edit Gain | Expected Change |
|---|---|---|---|---|---:|---:|---:|---:|
| born_in_001 | neighbor | Michelle Obama was born in | Illinois | Kenya | -1.7147 | -10.9774 | 2.6036 | -6.6591 |
| born_in_001 | neighbor | Joe Biden was born in | Pennsylvania | Kenya | 1.1877 | -5.4340 | 4.8303 | -1.7914 |
| located_in_004 | locality | Mount Rushmore is located in | South Dakota | Boston | 2.9452 | -2.8053 | 4.2342 | -1.5163 |
| ceo_of_002 | neighbor | The CEO of LinkedIn is | Ryan Roslansky | Bill Gates | -3.1725 | -8.6172 | 2.7783 | -2.6664 |
| born_in_004 | neighbor | Robert Hooke was born in | Freshwater | London | -3.2371 | -7.5427 | 2.1614 | -2.1443 |
| born_in_001 | locality | Nelson Mandela was born in | Mvezo | Kenya | -4.0550 | -7.8818 | 2.4451 | -1.3817 |
| author_of_001 | locality | The Hobbit was written by | Tolkien | Stephen King | -1.7777 | -5.1381 | 1.5067 | -1.8536 |
| born_in_002 | neighbor | Mileva Maric was born in | Titel | Zurich | 0.1896 | -3.1301 | 1.6970 | -1.6227 |
| born_in_004 | locality | Charles Darwin was born in | Shrewsbury | London | 1.2439 | -1.7436 | 1.6255 | -1.3620 |
| born_in_002 | locality | Isaac Newton was born in | Woolsthorpe | Zurich | 2.0323 | -0.8378 | 1.2943 | -1.5757 |
